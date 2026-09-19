from sqlalchemy.orm import Session

from app.repositories.business_attribute_score_repository import (
    get_business_attribute_scores
)


MIN_ATTRIBUTE_MENTIONS = 2

MAX_DISPLAY_ATTRIBUTES = 5


def calculate_confidence(
    mentions: int
):

    if mentions >= 10:

        return "high"


    if mentions >= 5:

        return "medium"


    return "low"



def get_business_attribute_summary(
    db: Session,
    business_id: int
):

    rows = get_business_attribute_scores(
        db,
        business_id
    )


    strengths = []
    weaknesses = []


    for score, attribute in rows:

        total = (
            score.positive_count +
            score.negative_count
        )


        # Attribute هایی که داده کافی ندارند نمایش داده نشوند
        if total < MIN_ATTRIBUTE_MENTIONS:
            continue


        positive_ratio = (
            score.positive_count / total
        )


        item = {

            "label": attribute.label,

            "mentions": total,

            "score": round(
                positive_ratio * 100,
                1
            ),

            "confidence": calculate_confidence(
                total
            )
        }


        if score.positive_count > score.negative_count:

            strengths.append(item)


        elif score.negative_count > score.positive_count:

            weaknesses.append(item)



    # نقاط قوت:
    # اول Score بالاتر، سپس تعداد Mention بیشتر
    strengths.sort(
        key=lambda x: (
            x["score"],
            x["mentions"]
        ),
        reverse=True
    )


    # نقاط ضعف:
    # اول Score پایین‌تر، سپس تعداد Mention بیشتر
    weaknesses.sort(
        key=lambda x: (
            x["score"],
            -x["mentions"]
        )
    )


    strengths = strengths[
        :MAX_DISPLAY_ATTRIBUTES
    ]


    weaknesses = weaknesses[
        :MAX_DISPLAY_ATTRIBUTES
    ]



    return {

        "strengths": strengths,

        "weaknesses": weaknesses

    }