from sqlalchemy.orm import Session


from app.repositories.business_repository import (
    get_business
)


from app.services.business_reputation_service import (
    get_business_reputation
)


from app.services.business_attribute_service import (
    get_business_attribute_summary
)




def get_public_business_profile(
    db: Session,
    business_id: int
):

    business = get_business(
        db=db,
        business_id=business_id
    )


    if not business:

        return None



    reputation = get_business_reputation(
        db=db,
        business_id=business_id
    )


    customer_insights = get_business_attribute_summary(
        db=db,
        business_id=business_id
    )



    return {

        "business": {

            "id": business.id,

            "name": business.name,

            "description": business.description,

            "phone": business.phone

        },


        "reputation": reputation,


        "customer_insights": customer_insights

    }