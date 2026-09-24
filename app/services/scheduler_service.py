from apscheduler.schedulers.background import BackgroundScheduler

from app.database.database import SessionLocal

from app.services.opportunity_expiration_service import (
    expire_old_opportunities
)

from app.services.commission_release_service import (
    release_due_commissions
)

from app.workers.review_ai_worker import (
    process_pending_review_ai_jobs
)



scheduler = BackgroundScheduler()


def run_opportunity_expiration():

    db = SessionLocal()

    try:

        result = expire_old_opportunities(
            db=db
        )

        print(
            f"Opportunity expiration executed: {result}"
        )

    finally:

        db.close()


def run_commission_release():

    db = SessionLocal()

    try:

        result = release_due_commissions(
            db=db
        )

        print(
            f"Commission release executed: {result}"
        )

    except Exception as exc:

        print(
            f"Commission release failed: {exc}"
        )

    finally:

        db.close()

def run_review_ai_worker():

    db = SessionLocal()

    try:

        process_pending_review_ai_jobs(
            db=db
        )


        print(
            "Review AI Worker executed"
        )


    except Exception as exc:

        print(
            f"Review AI Worker failed: {exc}"
        )


    finally:

        db.close()


def start_scheduler():

    scheduler.add_job(
        run_opportunity_expiration,
        trigger="interval",
        minutes=1,
        id="opportunity_expiration_job",
        replace_existing=True
    )

    scheduler.add_job(
        run_commission_release,
        trigger="interval",
        minutes=1,
        id="commission_release_job",
        replace_existing=True
    )
    scheduler.add_job(
        run_review_ai_worker,
        trigger="interval",
        minutes=1,
        id="review_ai_worker_job",
        replace_existing=True
    )
    scheduler.start()