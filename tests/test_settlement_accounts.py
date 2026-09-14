from app.database.database import SessionLocal

from app.services.settlement_service import (
    get_escrow_account,
    get_business_account,
    get_platform_treasury_account
)


db = SessionLocal()


escrow = get_escrow_account(db)

business = get_business_account(
    db,
    3
)

treasury = get_platform_treasury_account(db)



print("ESCROW")
print("----------------")
print(
    escrow.id if escrow else None,
    escrow.balance if escrow else None
)



print("BUSINESS")
print("----------------")
print(
    business.id if business else None,
    business.balance if business else None
)



print("TREASURY")
print("----------------")
print(
    treasury.id if treasury else None,
    treasury.balance if treasury else None
)



db.close()