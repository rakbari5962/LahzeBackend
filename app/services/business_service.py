from sqlalchemy.orm import Session


from app.repositories.business_repository import (
    create_business as create_business_repository
)


from app.repositories.business_service_repository import (
    create_business_service
)


from app.services.category_suggestion_service import (
    create_ai_category_suggestion
)


from app.schemas.business import BusinessCreate


from app.schemas.business_service import (
    BusinessServiceCreate
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