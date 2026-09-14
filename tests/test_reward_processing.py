import app.models

from app.database.database import SessionLocal

from app.services.referral_reward_service import (
    calculate_referral_rewards
)

from app.services.reward_processing_service import (
    process_referral_rewards
)


db = SessionLocal()


try:

    rewards = calculate_referral_rewards(
        db=db,
        business_id=2,
        platform_amount=50000
    )


    print("CALCULATED REWARDS")
    print("-------------------")

    for reward in rewards:
        print(
            reward["user_id"],
            reward["amount"]
        )


    processed = process_referral_rewards(
    db=db,
    rewards=rewards,
    business_id=2
    )


    print("")
    print("PROCESSED REWARDS")
    print("-----------------")


    for item in processed:

        print(
            item["user_id"],
            item["amount"]
        )


finally:

    db.close()