from sqlalchemy.orm import Session

from collections import defaultdict

from app.models.review_ai_result import ReviewAIResult



def get_main_negative_topic(
    db: Session,
    business_id: int
):

    results = db.query(
        ReviewAIResult
    ).filter(
        ReviewAIResult.business_id == business_id
    ).all()


    topics = defaultdict(
        lambda: {
            "mentions": 0,
            "negative_mentions": 0
        }
    )


    for result in results:

        for topic in result.topics:

            key = topic.get(
                "topic"
            )


            if not key:
                continue


            topics[key]["mentions"] += 1


            if topic.get("sentiment") == "negative":

                topics[key]["negative_mentions"] += 1



    if not topics:

        return None



    negative_topics = []


    for key, value in topics.items():

            if value["negative_mentions"] > 0:

                negative_percentage = round(
                    (
                        value["negative_mentions"]
                        /
                        value["mentions"]
                    )
                    *
                    100
                )


                negative_topics.append(
                    {
                        "topic": key,
                        "total_mentions": value["mentions"],
                        "negative_mentions": value["negative_mentions"],
                        "negative_percentage": negative_percentage
                    }
                )



    if not negative_topics:

        return None



    return max(
        negative_topics,
        key=lambda x: x["negative_mentions"]
    )