from app.database.database import SessionLocal

from app.services.settlement_service import settle_payment


db = SessionLocal()


try:

    result = settle_payment(
        db,
        booking_id=6,
        business_id=1,
        amount=1000000
    )


    print("TRANSACTION:")
    print(
        result["transaction"].transaction_id,
        result["transaction"].status
    )


    print("BUSINESS:")
    print(
        result["business_amount"]
    )


    print("PLATFORM:")
    print(
        result["platform_amount"]
    )


finally:

    db.close()