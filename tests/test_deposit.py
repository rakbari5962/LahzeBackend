from app.database.database import SessionLocal

from app.services.deposit_service import (
    deposit_to_user_wallet
)


db = SessionLocal()


try:

    result = deposit_to_user_wallet(
        db,
        user_id=3,
        amount=1000000
    )


    print("TRANSACTION:")
    print(
        result["transaction"].transaction_id,
        result["transaction"].status
    )


    print("WALLET:")
    print(
        result["wallet"].id,
        result["wallet"].balance
    )


    print("LEDGER:")
    print(
        result["ledger"].transaction_id,
        result["ledger"].amount
    )


finally:

    db.close()