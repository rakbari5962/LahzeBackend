from sqlalchemy.orm import Session


from app.services.deposit_service import (
    deposit_to_user_wallet
)


from app.repositories.reward_event_repository import (
    create_reward_event,
    complete_reward_event
)



def process_referral_rewards(
    db: Session,
    rewards: list,
    business_id: int,
    settlement_reference_id: int
):

    processed = []


    for reward in rewards:

        user_id = reward["user_id"]
        amount = reward["amount"]



        # Idempotency بر اساس Settlement واقعی
        # (Booking Settlement)

        idempotency_key = (
            f"SETTLEMENT-{settlement_reference_id}-{user_id}-REFERRAL_REWARD"
        )



        # ثبت Reward Event

        reward_event = create_reward_event(
            db=db,
            user_id=user_id,
            business_id=business_id,
            reward_type="REFERRAL_REWARD",
            amount=amount,
            idempotency_key=idempotency_key,
            status="PENDING"
        )


        if not reward_event:
            continue



        # جلوگیری از پرداخت دوباره

        if reward_event.status == "PROCESSED":

            print(
                "DUPLICATE REWARD EVENT:",
                user_id,
                reward_event.id,
                reward_event.status
            )


            processed.append(
                {
                    "user_id": user_id,
                    "amount": amount,
                    "reward_event": reward_event,
                    "duplicate": True
                }
            )

            continue



        # واریز به کیف پول

        transaction_result = deposit_to_user_wallet(
            db=db,
            user_id=user_id,
            amount=amount,
            transaction_type="REFERRAL_REWARD",
            reference_type="REFERRAL_REWARD"
        )


        print(
            "DEPOSIT RESULT FOR USER",
            user_id,
            ":",
            transaction_result
        )


        if not transaction_result:
            continue



        transaction = transaction_result["transaction"]



        # اتصال Reward Event به Transaction

        reward_event.transaction_id = (
            transaction.transaction_id
        )


        db.commit()

        db.refresh(reward_event)



        # تکمیل Reward Event

        reward_event = complete_reward_event(
            db=db,
            reward_event_id=reward_event.id
        )



        processed.append(
            {
                "user_id": user_id,
                "amount": amount,
                "reward_event": reward_event,
                "transaction": transaction_result
            }
        )


    return processed