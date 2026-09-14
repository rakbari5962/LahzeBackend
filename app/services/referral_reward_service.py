from sqlalchemy.orm import Session

from app.repositories.business_referral_share_repository import (
    get_active_shares
)



def calculate_referral_rewards(
    db: Session,
    business_id: int,
    platform_amount: int
):

    shares = get_active_shares(
        db,
        business_id
    )


    rewards = []


    for share in shares:

        reward_amount = (
            platform_amount
            *
            share.percentage
            //
            100
        )


        rewards.append(
            {
                "user_id": share.user_id,
                "amount": reward_amount,
                "type": "REFERRAL_REWARD"
            }
        )


    return rewards