from sqlalchemy.orm import Session

from app.repositories.business_attribute_score_repository import (
    get_business_attribute_scores
)


MIN_MENTIONS = 2
TOP_LIMIT = 3


def get_customer_insights(
    db: Session,
    business_id: int
):

    rows = get_business_attribute_scores(
        db=db,
        business_id=business_id
    )


    strengths = []
    improvements = []


    for score, attribute in rows:

        total_mentions = (
            score.positive_count +
            score.negative_count
        )


        if total_mentions < MIN_MENTIONS:
            continue


        total = total_mentions


        calculated_score = round(
            (score.positive_count / total) * 100
        )


        item = {

            "attribute_id": attribute.id,

            "key": attribute.key,

            "label": attribute.label,

            "score": calculated_score,

            "positive_count": score.positive_count,

            "negative_count": score.negative_count,

            "total_mentions": total_mentions

        }


        if calculated_score >= 80:

            strengths.append(item)


        elif calculated_score <= 50:

            improvements.append(item)



    strengths.sort(
        key=lambda x: x["total_mentions"],
        reverse=True
    )


    improvements.sort(
        key=lambda x: x["total_mentions"],
        reverse=True
    )


    return {

        "business_id": business_id,

        "summary": {

            "total_attributes": len(rows)

        },

        "strengths": strengths[:TOP_LIMIT],

        "improvements": improvements[:TOP_LIMIT]

    }