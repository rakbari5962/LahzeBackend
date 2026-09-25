from sqlalchemy.orm import Session

from app.repositories.business_attribute_score_repository import (
    get_business_attribute_scores
)


MIN_MENTIONS = 2
TOP_LIMIT = 10


def get_customer_insights(
    db: Session,
    business_id: int
):

    rows = get_business_attribute_scores(
        db=db,
        business_id=business_id
    )


    attributes = []


    for score, attribute in rows:


        total_mentions = (
            score.positive_count +
            score.negative_count
        )


        if total_mentions < MIN_MENTIONS:
            continue



        positive_percentage = round(
            (
                score.positive_count
                /
                total_mentions
            )
            * 100
        )


        negative_percentage = round(
            (
                score.negative_count
                /
                total_mentions
            )
            * 100
        )



        attributes.append({

            "attribute_id": attribute.id,

            "key": attribute.key,

            "label": attribute.label,

            "total_mentions": total_mentions,

            "positive_mentions": score.positive_count,

            "negative_mentions": score.negative_count,

            "positive_percentage": positive_percentage,

            "negative_percentage": negative_percentage

        })



    attributes.sort(
        key=lambda x: x["total_mentions"],
        reverse=True
    )



    return {

        "business_id": business_id,

        "summary": {

            "total_attributes": len(attributes)

        },

        "attributes": attributes[:TOP_LIMIT]

    }