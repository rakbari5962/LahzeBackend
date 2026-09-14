from app.database.database import SessionLocal


from app.services.settlement_service import (
    settle_payment
)


from app.services.wallet_service import (
    get_or_create_user_wallet
)



db = SessionLocal()



print("SETTLEMENT REWARD E2E TEST")
print("---------------------------")


result = settle_payment(
    db=db,
    booking_id=1001,
    business_id=3,
    amount=10000
)


print()


if result:

    print("SETTLEMENT SUCCESS")

    print(
        "Business:",
        result["business_amount"]
    )

    print(
        "Platform:",
        result["platform_amount"]
    )

else:

    print("SETTLEMENT FAILED")



print()


print("REFERRAL WALLETS")
print("----------------")


for user_id in [7,8]:

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



db.close()