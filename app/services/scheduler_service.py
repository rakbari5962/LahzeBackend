from apscheduler.schedulers.background import BackgroundScheduler


from app.database.database import SessionLocal


from app.services.opportunity_expiration_service import (
    expire_old_opportunities
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





def start_scheduler():


    scheduler.add_job(

        run_opportunity_expiration,

        trigger="interval",

        minutes=1,

        id="opportunity_expiration_job",

        replace_existing=True

    )


    scheduler.start()