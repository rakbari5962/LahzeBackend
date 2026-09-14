from app.database.database import SessionLocal

from app.services.account_service import create_escrow_account


db = SessionLocal()


try:

    escrow = create_escrow_account(
        db
    )


    print(
        escrow.id,
        escrow.owner_type,
        escrow.owner_id,
        escrow.account_type,
        escrow.balance
    )


finally:

    db.close()