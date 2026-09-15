from app.database.database import SessionLocal
from app.services.deposit_service import deposit_to_user_wallet


db = SessionLocal()

try:
    result = deposit_to_user_wallet(
        db=db,
        user_id=20,
        amount=3000000
    )

    print("DEPOSIT RESULT:")
    print(result)

    db.commit()

finally:
    db.close()