from app.services.account_service import (
    create_business_revenue_account
)

from sqlalchemy.orm import Session

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
    owner_user_id: int
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
        source_id=invitation.id
    )


def create_business(
    db: Session,
    business: BusinessCreate,
    owner_user_id: int
):

    db_business = create_business_repository(
        db=db,
        business=business,
        owner_user_id=owner_user_id
    )

    create_business_revenue_account(
        db=db,
        business_id=db_business.id
    )

    create_founder_inviter_attribution(
        db=db,
        business_id=db_business.id,
        owner_user_id=owner_user_id
    )

    if business.services:

        for service_name in business.services:

            create_business_service(
                db=db,
                business_id=db_business.id,
                service=BusinessServiceCreate(
                    name=service_name
                )
            )

    if business.services:

        create_ai_category_suggestion(
            db=db,
            business_id=db_business.id,
            business_name=business.name,
            services=business.services,
            description=business.description
        )

    return db_business
