from app.database.database import SessionLocal

from app.models.account import Account

from app.services.account_balance_service import increase_account_balance



db = SessionLocal()



# -------------------------
# Business Revenue Account
# -------------------------

business_account = Account(
    owner_type="BUSINESS",
    owner_id=3,
    account_type="BUSINESS_REVENUE",
    balance=0,
    currency="IRR",
    status="ACTIVE"
)


db.add(business_account)



# -------------------------
# Fund Escrow
# -------------------------

escrow = db.query(Account).filter(
    Account.owner_type=="PLATFORM",
    Account.account_type=="ESCROW"
).first()



db.commit()



if escrow:

    increase_account_balance(
        db,
        escrow.id,
        20000
    )



print("SETTLEMENT TEST ACCOUNTS CREATED")
print("---------------------------------")

print(
    "Business Account:",
    business_account.id
)

print(
    "Escrow:",
    escrow.id if escrow else None
)



db.close()