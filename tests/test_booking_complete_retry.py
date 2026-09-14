from app.database.database import SessionLocal

from app.repositories.booking_repository import (
    confirm_booking,
    complete_booking
)

from app.services.wallet_service import (
    get_user_wallet
)


db = SessionLocal()


BOOKING_ID = 7

REWARD_USER_ID = 3



def wallet_balance(user_id):

    wallet = get_user_wallet(
        db,
        user_id
    )

    return wallet.balance



print("BOOKING COMPLETE RETRY TEST")
print("============================")


print()
print("INITIAL WALLET")
print("----------------")

before = wallet_balance(
    REWARD_USER_ID
)

print(
    "User:",
    REWARD_USER_ID,
    "Balance:",
    before
)



print()
print("BOOKING COMPLETE #1")
print("----------------")


# reset flow
confirm_result = confirm_booking(
    db,
    BOOKING_ID
)


print(
    "CONFIRM:",
    confirm_result
)


complete_result = complete_booking(
    db,
    BOOKING_ID
)


print(
    "COMPLETE:",
    complete_result
)



after_first = wallet_balance(
    REWARD_USER_ID
)


print()
print("AFTER FIRST COMPLETE")
print("----------------")

print(
    "User:",
    REWARD_USER_ID,
    "Balance:",
    after_first
)



print()
print("BOOKING COMPLETE #2 RETRY")
print("----------------")


retry_result = complete_booking(
    db,
    BOOKING_ID
)


print(
    "RETRY:",
    retry_result
)



after_retry = wallet_balance(
    REWARD_USER_ID
)


print()
print("AFTER RETRY")
print("----------------")

print(
    "User:",
    REWARD_USER_ID,
    "Balance:",
    after_retry
)



if after_retry == after_first:

    print()
    print("IDEMPOTENCY PASSED ✅")

else:

    print()
    print("IDEMPOTENCY FAILED ❌")



db.close()