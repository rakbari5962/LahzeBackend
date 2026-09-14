from app.database.database import SessionLocal

from app.services.account_service import (
    initialize_platform_accounts
)


db = SessionLocal()


try:

    accounts = initialize_platform_accounts(
        db
    )


    for account in accounts:

        print(
            account.id,
            account.owner_type,
            account.owner_id,
            account.account_type,
            account.balance
        )


finally:

    db.close()