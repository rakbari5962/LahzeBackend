from app.services.account_service import (
    create_business_revenue_account
)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.business_category_repository import get_category

from app.repositories.business_repository import (
    create_business as create_business_repository,
    get_businesses_by_owner as get_businesses_by_owner_repository
)

from app.repositories.business_service_repository import (
    create_business_service
)

from app.repositories.business_priority_access_repository import (
    create_priority_access
)

from app.models.invitation import Invitation

from app.services.category_suggestion_service import (
    create_ai_category_suggestion
)

from app.schemas.business import BusinessCreate

from app.services.category_proposal_service import (
    attach_business_to_proposal
)

from app.schemas.business_service import (
    BusinessServiceCreate
)


def get_businesses_by_owner(
    db: Session,
    owner_user_id: int
):

    return get_businesses_by_owner_repository(
        db=db,
        owner_user_id=owner_user_id
    )


def create_founder_inviter_attribution(
    db: Session,
    business_id: int,
    owner_user_id: int,
    commit: bool = True
):

    invitation = (
        db.query(Invitation)
        .filter(
            Invitation.accepted_user_id == owner_user_id,
            Invitation.status == "ACCEPTED",
            Invitation.accepted_phone_match == True
        )
        .first()
    )

    if not invitation:
        return None

    return create_priority_access(
        db=db,
        business_id=business_id,
        user_id=invitation.inviter_user_id,
        access_type="FOUNDER_INVITER",
        source_id=invitation.id,
        commit=commit
    )


def create_business(
    db: Session,
    business: BusinessCreate,
    owner_user_id: int
):

    proposed_title = (business.proposed_category_title or "").strip()

    if proposed_title and business.category_id is not None:
        raise HTTPException(
            status_code=422,
            detail="فقط یکی از category_id یا proposed_category_title را ارسال کنید."
        )

    if business.category_id is not None:
        category = get_category(db, business.category_id)
        if category is None or not category.is_active:
            raise HTTPException(
                status_code=422,
                detail="دسته‌بندی انتخاب‌شده معتبر یا فعال نیست."
            )

    # One transaction for the whole registration: business, account,
    # attribution, services and (optionally) the quarantined proposal either
    # all commit or all roll back.
    proposal = None

    try:
        db_business = create_business_repository(
            db=db,
            business=business,
            owner_user_id=owner_user_id,
            commit=False
        )

        create_business_revenue_account(
            db=db,
            business_id=db_business.id,
            commit=False
        )

        create_founder_inviter_attribution(
            db=db,
            business_id=db_business.id,
            owner_user_id=owner_user_id,
            commit=False
        )

        for service_name in business.services:

            create_business_service(
                db=db,
                business_id=db_business.id,
                service=BusinessServiceCreate(
                    name=service_name
                ),
                commit=False
            )

        if proposed_title:

            _category, proposal = attach_business_to_proposal(
                db=db,
                raw_title=proposed_title,
                business=db_business
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    db.refresh(db_business)

    # Legacy rule-based suggestion for an existing category; skipped when the
    # user submitted a proposal or a category.
    if (
        business.services
        and business.category_id is None
        and db_business.category_id is None
        and proposal is None
    ):

        create_ai_category_suggestion(
            db=db,
            business_id=db_business.id,
            business_name=business.name,
            services=business.services,
            description=business.description
        )

    db_business.category_pending = proposal is not None
    db_business.proposal_id = proposal.id if proposal is not None else None

    return db_business
