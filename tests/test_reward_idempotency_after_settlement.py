from app.database.database import SessionLocal

from app.services.settlement_service import (
    settle_payment
)

from app.services.wallet_service import (
    get_user_wallet
)


db = SessionLocal()


BUSINESS_ID = 3

BOOKING_ID = 2001

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



print("REWARD IDEMPOTENCY AFTER SETTLEMENT TEST")
print("========================================")



print_wallets(
    "INITIAL WALLETS"
)



# -----------------------------
# Settlement اول
# -----------------------------

result_1 = settle_payment(
    db=db,
    booking_id=BOOKING_ID,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)


print()

if result_1:

    print("FIRST SETTLEMENT SUCCESS")

else:

    print("FIRST SETTLEMENT FAILED")



print_wallets(
    "AFTER FIRST SETTLEMENT"
)


from app.models.account import Account


escrow = db.query(Account).filter(
    Account.id == 5
).first()


escrow.balance = 30000

db.commit()

# -----------------------------
# همان Settlement دوباره Retry
# -----------------------------

result_2 = settle_payment(
    db=db,
    booking_id=BOOKING_ID,
    business_id=BUSINESS_ID,
    amount=AMOUNT
)



print()

if result_2:

    print("SECOND SETTLEMENT SUCCESS")

else:

    print("SECOND SETTLEMENT FAILED")



print_wallets(
    "AFTER SECOND SETTLEMENT RETRY"
)



db.close()