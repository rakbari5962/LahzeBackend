from sqlalchemy.orm import Session

from app.repositories.review_ai_analysis_repository import (
    get_public_business_analysis
)



def get_business_reputation(
    db: Session,
    business_id: int
):

    analysis = get_public_business_analysis(
        db,
        business_id
    )


    if not analysis:

        return None



    return {

        "business_id": analysis.business_id,

        "total_reviews": analysis.total_reviews,

        "average_rating": analysis.average_rating,

        "customer_sentiment": analysis.customer_sentiment or {},

        "model_version": analysis.model_version

    }