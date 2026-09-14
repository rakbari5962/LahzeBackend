from fastapi.testclient import TestClient

from app.main import app

from app.database.database import SessionLocal

from app.services.wallet_service import get_user_wallet


client = TestClient(app)


BOOKING_ID = 8
REWARD_USER_ID = 3



db = SessionLocal()



def wallet_balance(user_id):

    wallet = get_user_wallet(
        db,
        user_id
    )

    return wallet.balance



print("BOOKING COMPLETE API E2E TEST")
print("================================")


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
print("CONFIRM BOOKING API")
print("--------------------")


response = client.patch(
    f"/bookings/{BOOKING_ID}/confirm"
)


print(
    "STATUS:",
    response.status_code
)

print(
    response.json()
)



print()
print("COMPLETE BOOKING API")
print("---------------------")


response = client.patch(
    f"/bookings/{BOOKING_ID}/complete"
)


print(
    "STATUS:",
    response.status_code
)

print(
    response.json()
)



after = wallet_balance(
    REWARD_USER_ID
)



print()
print("FINAL WALLET")
print("----------------")

print(
    "User:",
    REWARD_USER_ID,
    "Balance:",
    after
)



if after > before:

    print()
    print("API FINANCIAL FLOW PASSED ✅")

else:

    print()
    print("API FINANCIAL FLOW FAILED ❌")



db.close()