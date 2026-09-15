from sqlalchemy.orm import Session

from app.repositories.business_referral_share_repository import (
    get_active_shares
)

from app.models.reward_event import RewardEvent



def create_booking_commissions(
    db: Session,
    business_id: int,
    booking_id: int,
    amount: int
):

    shares = get_active_shares(
        db,
        business_id
    )
    print(
        "COMMISSION SERVICE HIT:",
        business_id,
        booking_id,
        amount,
        "SHARES:",
        len(shares)
    )

    created_events = []


    for share in shares:

        commission_amount = int(
            amount * share.percentage / 100
        )


        if commission_amount <= 0:
            continue



        idempotency_key = (
            f"REFERRAL_COMMISSION_"
            f"BOOKING_{booking_id}_"
            f"USER_{share.user_id}"
        )


        existing_event = db.query(
            RewardEvent
        ).filter(
            RewardEvent.idempotency_key == idempotency_key
        ).first()



        if existing_event:
            created_events.append(
                existing_event
            )
            continue



        reward_event = RewardEvent(

            user_id=share.user_id,

            business_id=business_id,

            booking_id=booking_id,

            type="REFERRAL_COMMISSION",

            amount=commission_amount,

            status="PENDING",

            idempotency_key=idempotency_key

        )


        db.add(
            reward_event
        )


        created_events.append(
            reward_event
        )


    db.commit()


    for event in created_events:
        db.refresh(event)


    return created_events