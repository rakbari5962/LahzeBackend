import app.models

from app.database.database import SessionLocal

from app.services.referral_reward_service import (
    calculate_referral_rewards
)


db = SessionLocal()


try:

    rewards = calculate_referral_rewards(
        db=db,
        business_id=2,
        platform_amount=50000
    )


    print("REFERRAL REWARDS")
    print("----------------")


    for reward in rewards:

        print(
            "User:",
            reward["user_id"],
            "| Amount:",
            reward["amount"],
            "| Type:",
            reward["type"]
        )


finally:

    db.close()