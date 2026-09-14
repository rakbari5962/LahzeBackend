from sqlalchemy.orm import Session

from app.models.reward_event import RewardEvent



def create_reward_event(
    db: Session,
    user_id: int,
    reward_type: str,
    amount: int,
    idempotency_key: str,
    business_id: int = None,
    transaction_id: str = None,
    booking_id: int = None,
    status: str = "PENDING"
):


    existing_event = db.query(RewardEvent).filter(
        RewardEvent.idempotency_key == idempotency_key
    ).first()



    if existing_event:

        return existing_event



    reward_event = RewardEvent(

        user_id=user_id,

        business_id=business_id,

        transaction_id=transaction_id,

        booking_id=booking_id,

        idempotency_key=idempotency_key,

        type=reward_type,

        amount=amount,

        status=status

    )


    db.add(reward_event)

    db.commit()

    db.refresh(reward_event)


    return reward_event





def get_user_reward_events(
    db: Session,
    user_id: int
):

    return db.query(RewardEvent).filter(
        RewardEvent.user_id == user_id
    ).all()





def complete_reward_event(
    db: Session,
    reward_event_id: int
):

    event = db.query(RewardEvent).filter(
        RewardEvent.id == reward_event_id
    ).first()


    if not event:

        return None



    event.status = "PROCESSED"


    db.commit()

    db.refresh(event)


    return event