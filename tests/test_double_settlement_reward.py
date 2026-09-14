from app.database.database import SessionLocal

from app.services.settlement_service import (
    settle_payment
)

from app.services.wallet_service import (
    get_user_wallet
)



db = SessionLocal()



BUSINESS_ID = 3
BOOKING_1 = 1001
BOOKING_2 = 1002

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



print("DOUBLE SETTLEMENT REWARD TEST")
print("==============================")



print_wallets(
    "INITIAL WALLETS"
)



# -----------------------------
# Settlement شماره 1
# -----------------------------

result_1 = settle_payment(
    db=db,
    booking_id=BOOKING_1,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)


if result_1:

    print()
    print("SETTLEMENT #1 SUCCESS")

else:

    print()
    print("SETTLEMENT #1 FAILED")



print_wallets(
    "AFTER SETTLEMENT #1"
)



# -----------------------------
# Settlement شماره 2
# -----------------------------

result_2 = settle_payment(
    db=db,
    booking_id=BOOKING_2,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)


if result_2:

    print()
    print("SETTLEMENT #2 SUCCESS")

else:

    print()
    print("SETTLEMENT #2 FAILED")



print_wallets(
    "AFTER SETTLEMENT #2"
)



db.close()