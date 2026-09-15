from sqlalchemy.orm import Session


from app.models.reward_event import RewardEvent





def get_failed_release_history(
    db: Session
):


    errors = db.query(
        RewardEvent
    ).filter(

        RewardEvent.type == "REFERRAL_COMMISSION",

        RewardEvent.status == "FAILED"

    ).order_by(

        RewardEvent.created_at.desc()

    ).all()



    return errors