from sqlalchemy.orm import Session

from app.models.ledger import LedgerEntry



def create_ledger_entry(
    db: Session,
    account_id: int,
    transaction_id: str,
    entry_type: str,
    direction: str,
    amount: int,
    reference_type: str,
    reference_id: int
):

    ledger_entry = LedgerEntry(

        account_id=account_id,

        transaction_id=transaction_id,

        entry_type=entry_type,

        direction=direction,

        amount=amount,

        reference_type=reference_type,

        reference_id=reference_id

    )


    db.add(ledger_entry)

    db.commit()

    db.refresh(ledger_entry)


    return ledger_entry





def get_account_ledger(
    db: Session,
    account_id: int
):

    return db.query(LedgerEntry).filter(
        LedgerEntry.account_id == account_id
    ).order_by(
        LedgerEntry.created_at.desc()
    ).all()





def get_transaction_entries(
    db: Session,
    transaction_id: str
):

    return db.query(LedgerEntry).filter(
        LedgerEntry.transaction_id == transaction_id
    ).all()