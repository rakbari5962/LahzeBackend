from app.database.database import SessionLocal

from app.services.reward_processing_service import (
    process_referral_rewards
)

from app.services.wallet_service import (
    get_or_create_user_wallet
)



db = SessionLocal()



# Reward اولیه

rewards = [
    {
        "user_id": 4,
        "amount": 500
    },
    {
        "user_id": 5,
        "amount": 500
    }
]



business_id = 2



print("FIRST PROCESS")
print("----------------")


first = process_referral_rewards(
    db=db,
    rewards=rewards,
    business_id=business_id
)


for item in first:

    print(
        item["user_id"],
        item["amount"]
    )



print()



print("SECOND PROCESS")
print("----------------")


second = process_referral_rewards(
    db=db,
    rewards=rewards,
    business_id=business_id
)


for item in second:

    print(
        item["user_id"],
        item["amount"]
    )



print()



print("WALLETS")
print("----------------")



for user_id in [4, 5]:

    wallet = get_or_create_user_wallet(
        db,
        user_id
    )

    print(
        "User:",
        user_id,
        "Balance:",
        wallet.balance
    )