from sqlalchemy.orm import Session


from app.repositories.business_priority_access_repository import (
    get_business_priority_accesses
)


from app.repositories.reward_event_repository import (
    create_reward_event
)


from app.services.deposit_service import (
    deposit_to_user_wallet
)



def trigger_priority_access_rewards(
    db: Session,
    business_id: int,
    booking_id: int,
    amount: int
):


    if amount <= 0:
        return []



    accesses = get_business_priority_accesses(
        db=db,
        business_id=business_id
    )


    if not accesses:
        return []



    processed = []



    reward_amount = int(
        amount * 0.01
    )



    for access in accesses:


        if access.status != "ACTIVE":
            continue



        idempotency_key = (
            f"PRIORITY-{booking_id}-"
            f"{access.user_id}-"
            f"{access.type}"
        )



        reward_event = create_reward_event(
            db=db,
            user_id=access.user_id,
            business_id=business_id,
            booking_id=booking_id,
            reward_type=access.type + "_REWARD",
            amount=reward_amount,
            idempotency_key=idempotency_key,
            status="PENDING"
        )



        if not reward_event:
            continue



        if reward_event.status == "PROCESSED":

            processed.append(
                {
                    "user_id": access.user_id,
                    "amount": reward_amount,
                    "duplicate": True
                }
            )

            continue



        transaction_result = deposit_to_user_wallet(
            db=db,
            user_id=access.user_id,
            amount=reward_amount,
            transaction_type=access.type + "_REWARD",
            reference_type="PRIORITY_ACCESS"
        )



        if not transaction_result:
            continue



        transaction = transaction_result["transaction"]



        reward_event.transaction_id = (
            transaction.transaction_id
        )


        db.commit()

        db.refresh(reward_event)



        reward_event.status = "PROCESSED"


        db.commit()

        db.refresh(reward_event)



        processed.append(
            {
                "user_id": access.user_id,
                "type": access.type,
                "amount": reward_amount,
                "reward_event_id": reward_event.id
            }
        )



    return processed