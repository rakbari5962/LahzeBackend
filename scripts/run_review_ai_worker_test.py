from app.database.database import SessionLocal

from app.workers.review_ai_worker import (
    process_pending_review_ai_jobs
)


db = SessionLocal()


try:

    process_pending_review_ai_jobs(
        db=db
    )


finally:

    db.close()