from sqlalchemy.orm import Session

from app.services.customer_insight_service import (
    get_customer_insights
)


def get_business_insight(
    db: Session,
    business_id: int
):

    insights = get_customer_insights(
        db=db,
        business_id=business_id
    )


    strengths = []

    improvements = []


    for item in insights.get("strengths", []):

        strengths.append(
            {
                "name": item["key"],
                "label": item["label"],
                "mentions": item["total_mentions"],
                "positive_mentions": item["positive_mentions"]
            }
        )


    for item in insights.get("improvements", []):

        improvements.append(
            {
                "topic": item["key"],
                "label": item["label"],
                "total_mentions": item["total_mentions"],
                "negative_mentions": item["negative_mentions"],
                "negative_percentage": round(
                    (
                        item["negative_mentions"]
                        /
                        item["total_mentions"]
                    )
                    * 100
                )
                if item["total_mentions"]
                else 0,
                "summary": (
                    f"{item['negative_mentions']} مورد از "
                    f"{item['total_mentions']} تجربه مشتریان درباره "
                    f"{item['label']} بازخورد منفی داشته‌اند "
                    f"({round((item['negative_mentions'] / item['total_mentions']) * 100)}٪)."
                )
            }
        )


    return {

        "business_id": business_id,

        "total_reviews": 0,

        "average_rating": None,

        "strengths": strengths,

        "weaknesses": improvements,

        "themes": [],

        "customer_sentiment": {},

        "attribute_summary": {},

        "model_version": "aggregation-v2"

    }