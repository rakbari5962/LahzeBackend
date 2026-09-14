from sqlalchemy.orm import Session

from app.models.account import Account



def get_account_balance(
    db: Session,
    account_id: int
):

    account = db.query(Account).filter(
        Account.id == account_id
    ).first()


    if not account:
        return None


    return account.balance





def increase_account_balance(
    db: Session,
    account_id: int,
    amount: int
):

    account = db.query(Account).filter(
        Account.id == account_id
    ).first()


    if not account:
        return None


    if amount <= 0:
        return None


    account.balance += amount


    db.commit()

    db.refresh(account)


    return account





def decrease_account_balance(
    db: Session,
    account_id: int,
    amount: int
):

    account = db.query(Account).filter(
        Account.id == account_id
    ).first()


    if not account:
        return None


    if amount <= 0:
        return None


    if account.balance < amount:
        return None


    account.balance -= amount


    db.commit()

    db.refresh(account)


    return account