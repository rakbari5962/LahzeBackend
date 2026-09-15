from sqlalchemy.orm import Session


from app.models.reward_event import RewardEvent





def get_release_history(
    db: Session
):


    releases = db.query(
        RewardEvent
    ).filter(

        RewardEvent.type == "REFERRAL_COMMISSION",

        RewardEvent.status == "PROCESSED"

    ).order_by(

        RewardEvent.created_at.desc()

    ).all()



    return releases