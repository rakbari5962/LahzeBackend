from app.database.database import SessionLocal

from app.repositories.booking_repository import (
    confirm_booking,
    complete_booking
)

from app.services.wallet_service import (
    get_user_wallet
)



db = SessionLocal()



BOOKING_ID = 1



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



print("BOOKING COMPLETE FINANCIAL E2E TEST")
print("====================================")



print_wallets(
    "INITIAL WALLET"
)



print()
print("CONFIRM BOOKING")
print("----------------")


confirmed = confirm_booking(
    db,
    BOOKING_ID
)


print(
    confirmed
)



print()
print("COMPLETE BOOKING")
print("----------------")


completed = complete_booking(
    db,
    BOOKING_ID
)


print(
    completed
)



print_wallets(
    "FINAL WALLET"
)



db.close()