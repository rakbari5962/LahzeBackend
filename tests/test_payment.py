from app.database.database import SessionLocal

from app.services.payment_service import create_payment


db = SessionLocal()


try:

    result = create_payment(
        db,
        user_id=3,
        amount=1000000,
        booking_id=6
    )


    print("TRANSACTION:")
    print(
        result["transaction"].transaction_id,
        result["transaction"].status
    )


    print("DEBIT:")
    print(
        result["debit"].account_id,
        result["debit"].amount
    )


    print("CREDIT:")
    print(
        result["credit"].account_id,
        result["credit"].amount
    )


finally:

    db.close()