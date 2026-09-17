from app.services.account_service import (
    create_business_revenue_account
)

from sqlalchemy.orm import Session


from app.repositories.business_repository import (
    create_business as create_business_repository
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


    # ساخت کسب و کار

    db_business = create_business_repository(

        db=db,

        business=business,

        owner_user_id=owner_user_id

    )

    # ساخت حساب درآمد کسب و کار
    
    create_business_revenue_account(
        db=db,
        business_id=db_business.id
    )



    # ثبت Founder Inviter Attribution

    create_founder_inviter_attribution(

        db=db,

        business_id=db_business.id,

        owner_user_id=owner_user_id

    )



    # ذخیره خدمات کسب و کار

    if business.services:


        for service_name in business.services:


            create_business_service(

                db=db,

                business_id=db_business.id,

                service=BusinessServiceCreate(

                    name=service_name

                )

            )



    # ساخت پیشنهاد AI دسته بندی

    if business.services:


        create_ai_category_suggestion(

            db=db,

            business_id=db_business.id,

            business_name=business.name,

            services=business.services,

            description=business.description

        )



    return db_business