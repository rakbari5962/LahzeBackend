from sqlalchemy.orm import Session

from app.models.review_ai_job import ReviewAIJob



def create_review_ai_job(
    db: Session,
    review_id: int,
    business_id: int
):

    job = ReviewAIJob(

        review_id=review_id,

        business_id=business_id,

        status="pending",

        retry_count=0

    )


    db.add(job)

    db.commit()

    db.refresh(job)


    return job





def get_job_by_review_id(
    db: Session,
    review_id: int
):

    return (
        db.query(ReviewAIJob)
        .filter(
            ReviewAIJob.review_id == review_id
        )
        .first()
    )





def get_pending_jobs(
    db: Session,
    limit: int = 10
):

    return (
        db.query(ReviewAIJob)
        .filter(
            ReviewAIJob.status == "pending"
        )
        .order_by(
            ReviewAIJob.created_at
        )
        .limit(limit)
        .all()
    )





def mark_job_processing(
    db: Session,
    job: ReviewAIJob
):

    job.status = "processing"

    db.commit()

    db.refresh(job)

    return job





def mark_job_completed(
    db: Session,
    job: ReviewAIJob
):

    job.status = "completed"

    db.commit()

    db.refresh(job)

    return job





def mark_job_failed(
    db: Session,
    job: ReviewAIJob,
    error: str
):

    job.status = "failed"

    job.last_error = error

    job.retry_count += 1

    db.commit()

    db.refresh(job)

    return job