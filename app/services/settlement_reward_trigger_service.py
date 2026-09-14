from sqlalchemy.orm import Session


from app.services.referral_reward_service import (
    calculate_referral_rewards
)


from app.services.reward_processing_service import (
    process_referral_rewards
)



def trigger_settlement_rewards(
    db: Session,
    business_id: int,
    platform_amount: int,
    settlement_reference_id: int
):


    # 1. محاسبه Reward معرف‌ها

    rewards = calculate_referral_rewards(
        db=db,
        business_id=business_id,
        platform_amount=platform_amount
    )


    print(
        "CALCULATED SETTLEMENT REWARDS:",
        rewards
    )


    if not rewards:
        return []



    # 2. پردازش Rewardها

    processed = process_referral_rewards(
        db=db,
        rewards=rewards,
        business_id=business_id,
        settlement_reference_id=settlement_reference_id
    )


    return processed