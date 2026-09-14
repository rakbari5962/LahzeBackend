from sqlalchemy.orm import Session

from app.models.account import Account



def create_account(
    db: Session,
    owner_type: str,
    owner_id: int,
    account_type: str,
    currency: str = "IRR"
):

    existing_account = db.query(Account).filter(
        Account.owner_type == owner_type,
        Account.owner_id == owner_id,
        Account.account_type == account_type
    ).first()


    if existing_account:
        return existing_account



    account = Account(

        owner_type=owner_type,

        owner_id=owner_id,

        account_type=account_type,

        balance=0,

        currency=currency,

        status="ACTIVE"

    )


    db.add(account)

    db.commit()

    db.refresh(account)


    return account





def get_account(
    db: Session,
    account_id: int
):

    return db.query(Account).filter(
        Account.id == account_id
    ).first()





def get_owner_account(
    db: Session,
    owner_type: str,
    owner_id: int,
    account_type: str
):

    return db.query(Account).filter(
        Account.owner_type == owner_type,
        Account.owner_id == owner_id,
        Account.account_type == account_type
    ).first()





def get_platform_treasury(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "PLATFORM_TREASURY"
    ).first()