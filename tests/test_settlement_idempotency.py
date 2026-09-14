from app.database.database import SessionLocal

from app.services.settlement_service import (
    settle_payment
)

from app.services.wallet_service import (
    get_user_wallet
)



db = SessionLocal()


BUSINESS_ID = 3

BOOKING_ID = 3001

AMOUNT = 10000



def print_wallets(title):

    print()
    print(title)
    print("----------------")

    for user_id in [7, 8]:

        wallet = get_user_wallet(
            db,
            user_id
        )

        print(
            "User:",
            user_id,
            "Balance:",
            wallet.balance
        )



print("SETTLEMENT IDEMPOTENCY TEST")
print("============================")


print_wallets(
    "INITIAL WALLET"
)



print()
print("FIRST SETTLEMENT")
print("----------------")


first = settle_payment(
    db=db,
    booking_id=BOOKING_ID,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)


print(first)



print_wallets(
    "AFTER FIRST SETTLEMENT"
)



print()
print("SECOND SETTLEMENT RETRY")
print("------------------------")


second = settle_payment(
    db=db,
    booking_id=BOOKING_ID,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)


print(second)



print_wallets(
    "AFTER SECOND RETRY"
)



db.close()