from sqlalchemy.orm import Session

from app.models.review_ai_result import ReviewAIResult



def save_review_ai_result(
    db: Session,
    review_id: int,
    business_id: int,
    result: dict
):

    existing = db.query(
        ReviewAIResult
    ).filter(
        ReviewAIResult.review_id == review_id
    ).first()


    if existing:

        existing.topics = result.get(
            "topics",
            []
        )

        existing.sentiment = result.get(
            "sentiment",
            {}
        )

        existing.raw_response = result

        existing.model_version = (
            "llm-aggregation-v2"
        )


        db.commit()

        db.refresh(existing)

        return existing



    analysis = ReviewAIResult(

        review_id=review_id,

        business_id=business_id,

        topics=result.get(
            "topics",
            []
        ),

        sentiment=result.get(
            "sentiment",
            {}
        ),

        raw_response=result,

        model_version="llm-aggregation-v2"

    )


    db.add(analysis)

    db.commit()

    db.refresh(analysis)


    return analysis