from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security.admin_guard import admin_required
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.category_proposal import (
    CategoryProposalDetailResponse,
    CategoryProposalPage,
    CategoryProposalRejectRequest,
    CategoryProposalApproveRequest,
    CategoryProposalResponse,
)
from app.services import category_proposal_service as service


router = APIRouter(
    prefix="/admin/category-proposals",
    tags=["Admin Category Proposals"],
)


def _summary(proposal) -> dict:
    return {
        "id": proposal.id,
        "title": proposal.title,
        "source": proposal.source,
        "status": proposal.status,
        "final_category_id": proposal.final_category_id,
        "reviewed_by_user_id": proposal.reviewed_by_user_id,
        "review_note": proposal.review_note,
        "created_at": proposal.created_at,
    }


def _detail(db: Session, proposal) -> dict:
    data = _summary(proposal)
    data["businesses"] = service.get_linked_businesses(db, proposal.id)
    data["history"] = service.get_proposal_history(db, proposal.id)
    data["possible_matches"] = service.get_possible_matches(db, proposal)
    return data


@router.get("/", response_model=CategoryProposalPage)
def list_category_proposals(
    status: str | None = Query(default="PENDING"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _admin: User = Depends(admin_required),
):
    items, total = service.list_proposals(db, status, page, page_size)
    return {
        "items": [_summary(item) for item in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/{proposal_id}", response_model=CategoryProposalDetailResponse)
def get_category_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(admin_required),
):
    return _detail(db, service.get_proposal_detail(db, proposal_id))


@router.post("/{proposal_id}/approve", response_model=CategoryProposalResponse)
def approve_category_proposal(
    proposal_id: int,
    data: CategoryProposalApproveRequest | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    proposal = service.approve_proposal(
        db,
        proposal_id=proposal_id,
        admin_user_id=admin.id,
        note=data.note if data else None,
    )
    return _summary(proposal)


@router.post("/{proposal_id}/reject", response_model=CategoryProposalResponse)
def reject_category_proposal(
    proposal_id: int,
    data: CategoryProposalRejectRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    proposal = service.reject_proposal_with_replacement(
        db,
        proposal_id=proposal_id,
        admin_user_id=admin.id,
        replacement_title=data.replacement_title,
        note=data.note,
    )
    return _summary(proposal)
