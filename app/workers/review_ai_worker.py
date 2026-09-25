from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.review_ai_job import ReviewAIJob
from app.models.review import Review

from app.services.gemini_review_analysis_service import (
    analyze_review_with_gemini
)

from app.services.review_attribute_service import (
    process_review_attributes
)

from app.repositories.review_ai_result_repository import (
    save_review_ai_result
)

from app.services.review_ai_result_aggregation_service import (
    get_main_negative_topic
)

from app.repositories.review_ai_analysis_repository import (
    update_main_business_issue
)




def process_pending_review_ai_jobs(
    db: Session
):

    jobs = db.query(
        ReviewAIJob
    ).filter(
        ReviewAIJob.status == "pending"
    ).order_by(
        ReviewAIJob.created_at.asc()
    ).all()


    for job in jobs:

        try:

            print(
                "PROCESSING AI JOB:",
                job.id,
                "REVIEW:",
                job.review_id
            )


            job.status = "processing"

            db.commit()



            review = db.query(
                Review
            ).filter(
                Review.id == job.review_id
            ).first()



            if not review:

                raise Exception(
                    "Review not found"
                )



            result = analyze_review_with_gemini(
                review.comment,
                review.rating
            )
            topic_labels = {
                "waiting_time": "زمان انتظار",
                "quality": "کیفیت خدمات",
                "staff_behavior": "برخورد پرسنل"
            }


            for topic in result.get("topics", []):

                topic["label"] = topic_labels.get(
                    topic.get("topic"),
                    topic.get("topic")
                )

            save_review_ai_result(
                db=db,
                review_id=review.id,
                business_id=review.business_id,
                result=result
            )

            issue = get_main_negative_topic(
                db=db,
                business_id=review.business_id
            )

            print(
                "MAIN ISSUE FROM AGGREGATOR:",
                issue
            )

            if issue:

                update_main_business_issue(
                    db=db,
                    business_id=review.business_id,
                    issue=issue
                )

            

            topics = result.get(
                "topics",
                []
            )


            attributes = []


            for item in topics:

                attributes.append(
                    {
                        "key": item.get("topic"),
                        "label": item.get("label"),
                        "sentiment": item.get("sentiment")
                    }
                )



            if attributes:

                process_review_attributes(
                    db=db,
                    business_id=review.business_id,
                    attributes=attributes
                )



            job.status = "completed"

            job.processed_at = datetime.now(
                timezone.utc
            )


            db.commit()



            print(
                "AI JOB COMPLETED:",
                job.id
            )



        except Exception as e:


            job.status = "failed"

            job.retry_count += 1

            job.last_error = str(e)


            db.commit()



            print(
                "AI JOB FAILED:",
                job.id,
                str(e)
            )