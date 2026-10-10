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
    amount: int,
    commit: bool = True,
):
    if amount <= 0:
        return None

    account = db.query(Account).filter(
        Account.id == account_id
    ).first()

    if not account:
        return None

    # Atomic SQL arithmetic prevents concurrent credits from overwriting
    # one another's balance changes.
    updated = db.query(Account).filter(
        Account.id == account_id
    ).update(
        {Account.balance: Account.balance + amount},
        synchronize_session=False,
    )

    if updated != 1:
        return None

    if commit:
        db.commit()
    else:
        db.flush()

    db.refresh(account)
    return account


def decrease_account_balance(
    db: Session,
    account_id: int,
    amount: int,
    commit: bool = True,
):
    if amount <= 0:
        return None

    account = db.query(Account).filter(
        Account.id == account_id
    ).first()

    if not account:
        return None

    # Check available funds and subtract in one SQL statement.
    updated = db.query(Account).filter(
        Account.id == account_id,
        Account.balance >= amount,
    ).update(
        {Account.balance: Account.balance - amount},
        synchronize_session=False,
    )

    if updated != 1:
        return None

    if commit:
        db.commit()
    else:
        db.flush()

    db.refresh(account)
    return account
