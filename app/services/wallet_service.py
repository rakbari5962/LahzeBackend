from sqlalchemy.orm import Session

from app.models.account import Account
from app.repositories.account_repository import create_account



def get_user_wallet(
    db: Session,
    user_id: int
):

    return db.query(Account).filter(
        Account.owner_type == "USER",
        Account.owner_id == user_id,
        Account.account_type == "CUSTOMER_WALLET"
    ).first()





def create_user_wallet(
    db: Session,
    user_id: int
):

    existing_wallet = get_user_wallet(
        db,
        user_id
    )


    if existing_wallet:
        return existing_wallet



    return create_account(
        db,
        owner_type="USER",
        owner_id=user_id,
        account_type="CUSTOMER_WALLET"
    )





def get_or_create_user_wallet(
    db: Session,
    user_id: int
):

    wallet = get_user_wallet(
        db,
        user_id
    )


    if wallet:
        return wallet


    return create_user_wallet(
        db,
        user_id
    )