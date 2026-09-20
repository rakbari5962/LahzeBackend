from sqlalchemy.orm import Session


from app.repositories.business_repository import (
    get_business
)


from app.services.business_reputation_service import (
    get_business_reputation
)


from app.services.customer_insight_service import (
    get_customer_insights
)


from app.services.customer_experience_formatter import (
    format_customer_experience
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





    raw_insights = get_customer_insights(
        db=db,
        business_id=business_id
    )


    print("RAW INSIGHTS:")
    print(raw_insights)





    customer_experience = format_customer_experience(
        raw_insights
    )


    print("CUSTOMER EXPERIENCE:")
    print(customer_experience)





    return {

        "business": {

            "id": business.id,

            "name": business.name,

            "description": business.description,

            "phone": business.phone

        },


        "reputation": reputation,


        "customer_experience": customer_experience

    }