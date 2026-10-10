from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.business_category import BusinessCategory
from app.models.category_proposal import (
    PROPOSAL_APPROVED,
    PROPOSAL_PENDING,
    PROPOSAL_REJECTED_REPLACED,
    CategoryProposal,
    CategoryProposalBusiness,
    CategoryProposalHistory,
)
from app.services.category_normalization import slugify_category, validate_category_title
from app.services.category_resolution_service import find_existing_category, find_near_duplicates


def _bad_title(exc: ValueError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(exc))


def get_pending_proposal_by_title(db: Session, normalized_title: str):
    return (
        db.query(CategoryProposal)
        .filter(
            CategoryProposal.normalized_title == normalized_title,
            CategoryProposal.status == PROPOSAL_PENDING,
        )
        .first()
    )


def attach_business_to_proposal(db: Session, raw_title: str, business: Business):
    """Registration-time step. Never commits; the caller owns the transaction.

    Returns (category, proposal). Exactly one is not None:
    - an equivalent category now exists -> assign it, no proposal
    - otherwise -> find or create the PENDING proposal and link the business,
      leaving business.category_id NULL
    """
    try:
        title, normalized = validate_category_title(raw_title)
    except ValueError as exc:
        raise _bad_title(exc)

    category, _match = find_existing_category(db, normalized)
    if category is not None:
        business.category_id = category.id
        return category, None

    proposal = get_pending_proposal_by_title(db, normalized)
    if proposal is None:
        try:
            # Savepoint: a lost race on the partial unique index must not roll
            # back the business that is being registered.
            with db.begin_nested():
                proposal = CategoryProposal(
                    title=title,
                    normalized_title=normalized,
                    source="LLM",
                    status=PROPOSAL_PENDING,
                )
                db.add(proposal)
                db.flush()
        except IntegrityError:
            proposal = get_pending_proposal_by_title(db, normalized)
            if proposal is None:
                raise

    link_exists = (
        db.query(CategoryProposalBusiness.id)
        .filter(
            CategoryProposalBusiness.proposal_id == proposal.id,
            CategoryProposalBusiness.business_id == business.id,
        )
        .first()
    )
    if link_exists is None:
        db.add(CategoryProposalBusiness(proposal_id=proposal.id, business_id=business.id))
        db.flush()

    return None, proposal


def get_pending_proposal_for_business(db: Session, business_id: int):
    return (
        db.query(CategoryProposal)
        .join(CategoryProposalBusiness, CategoryProposalBusiness.proposal_id == CategoryProposal.id)
        .filter(
            CategoryProposalBusiness.business_id == business_id,
            CategoryProposal.status == PROPOSAL_PENDING,
        )
        .first()
    )


# ---------------------------------------------------------------- admin review

def list_proposals(db: Session, status: str | None, page: int, page_size: int):
    query = db.query(CategoryProposal)
    if status:
        query = query.filter(CategoryProposal.status == status)
    total = query.count()
    items = (
        query.order_by(CategoryProposal.created_at.asc(), CategoryProposal.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total


def get_proposal_detail(db: Session, proposal_id: int):
    proposal = db.query(CategoryProposal).filter(CategoryProposal.id == proposal_id).first()
    if proposal is None:
        raise HTTPException(status_code=404, detail="PROPOSAL_NOT_FOUND")
    return proposal


def get_linked_businesses(db: Session, proposal_id: int):
    return (
        db.query(Business)
        .join(CategoryProposalBusiness, CategoryProposalBusiness.business_id == Business.id)
        .filter(CategoryProposalBusiness.proposal_id == proposal_id)
        .order_by(Business.id.asc())
        .all()
    )


def get_proposal_history(db: Session, proposal_id: int):
    return (
        db.query(CategoryProposalHistory)
        .filter(CategoryProposalHistory.proposal_id == proposal_id)
        .order_by(CategoryProposalHistory.id.asc())
        .all()
    )


def get_possible_matches(db: Session, proposal: CategoryProposal):
    return find_near_duplicates(db, proposal.normalized_title)


def _lock_pending_proposal(db: Session, proposal_id: int) -> CategoryProposal:
    proposal = (
        db.query(CategoryProposal)
        .filter(CategoryProposal.id == proposal_id)
        .with_for_update()
        .first()
    )
    if proposal is None:
        raise HTTPException(status_code=404, detail="PROPOSAL_NOT_FOUND")
    if proposal.status != PROPOSAL_PENDING:
        raise HTTPException(status_code=409, detail="PROPOSAL_NOT_PENDING")
    return proposal


def _unique_slug(db: Session, base: str) -> str:
    slug = base
    suffix = 2
    while db.query(BusinessCategory.id).filter(BusinessCategory.slug == slug).first():
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug


def _resolve_or_create_category(db: Session, title: str, normalized: str) -> BusinessCategory:
    """Reuse an equivalent category or create one. Flushes, never commits."""
    existing, _match = find_existing_category(db, normalized)
    if existing is not None:
        return existing

    try:
        with db.begin_nested():
            category = BusinessCategory(
                name=title,
                normalized_name=normalized,
                slug=_unique_slug(db, slugify_category(normalized)),
                description=None,
                is_active=True,
            )
            db.add(category)
            db.flush()
        return category
    except IntegrityError:
        existing, _match = find_existing_category(db, normalized)
        if existing is None:
            raise
        return existing


def _assign_category_to_linked_businesses(db: Session, proposal_id: int, category: BusinessCategory):
    businesses = (
        db.query(Business)
        .join(CategoryProposalBusiness, CategoryProposalBusiness.business_id == Business.id)
        .filter(CategoryProposalBusiness.proposal_id == proposal_id)
        .with_for_update()
        .all()
    )
    for business in businesses:
        if business.is_deleted:
            continue
        if business.category_id is None:
            business.category_id = category.id
        elif business.category_id != category.id:
            # Changed by another operation since the proposal; do not overwrite.
            raise HTTPException(
                status_code=409,
                detail={"error": "BUSINESS_CATEGORY_CHANGED", "business_id": business.id},
            )
    return businesses


def _finish(
    db: Session,
    proposal: CategoryProposal,
    category: BusinessCategory,
    new_status: str,
    decision: str,
    admin_user_id: int,
    note: str | None,
    replacement_title: str | None,
):
    previous_status = proposal.status
    proposal.status = new_status
    proposal.final_category_id = category.id
    proposal.reviewed_by_user_id = admin_user_id
    proposal.reviewed_at = datetime.now(timezone.utc)
    proposal.review_note = note

    db.add(
        CategoryProposalHistory(
            proposal_id=proposal.id,
            original_title=proposal.title,
            from_status=previous_status,
            to_status=new_status,
            decision=decision,
            admin_user_id=admin_user_id,
            replacement_title=replacement_title,
            final_category_id=category.id,
            note=note,
        )
    )
    db.flush()


def approve_proposal(db: Session, proposal_id: int, admin_user_id: int, note: str | None = None):
    """One transaction: lock, resolve/create category, assign, status, history."""
    try:
        proposal = _lock_pending_proposal(db, proposal_id)
        category = _resolve_or_create_category(db, proposal.title, proposal.normalized_title)
        _assign_category_to_linked_businesses(db, proposal.id, category)
        _finish(db, proposal, category, PROPOSAL_APPROVED, "APPROVED", admin_user_id, note, None)
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(proposal)
    return proposal


def reject_proposal_with_replacement(
    db: Session,
    proposal_id: int,
    admin_user_id: int,
    replacement_title: str,
    note: str | None = None,
):
    """The administrator's replacement, not the original title, becomes the category."""
    try:
        display, normalized = validate_category_title(replacement_title)
    except ValueError as exc:
        raise _bad_title(exc)

    try:
        proposal = _lock_pending_proposal(db, proposal_id)
        category = _resolve_or_create_category(db, display, normalized)
        _assign_category_to_linked_businesses(db, proposal.id, category)
        _finish(
            db,
            proposal,
            category,
            PROPOSAL_REJECTED_REPLACED,
            "REJECTED_WITH_REPLACEMENT",
            admin_user_id,
            note,
            display,
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(proposal)
    return proposal
