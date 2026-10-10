from sqlalchemy.orm import Session

from app.repositories.financial_transaction_repository import (
    create_transaction,
    get_transaction,
    update_transaction_status
)



def create_financial_transaction(
    db: Session,
    transaction_id: str,
    transaction_type: str,
    amount: int,
    reference_type: str,
    reference_id: int,
    commit: bool = True,
    fail_if_exists: bool = False,
):
    transaction = create_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_type=transaction_type,
        total_amount=amount,
        reference_type=reference_type,
        reference_id=reference_id,
        commit=commit,
        fail_if_exists=fail_if_exists,
    )

    return transaction





def complete_financial_transaction(
    db: Session,
    transaction_id: str,
    commit: bool = True,
):
    return update_transaction_status(
        db,
        transaction_id,
        "COMPLETED",
        commit=commit,
    )






def fail_financial_transaction(
    db: Session,
    transaction_id: str
):

    return update_transaction_status(
        db,
        transaction_id,
        "FAILED"
    )





def get_financial_transaction(
    db: Session,
    transaction_id: str
):

    return get_transaction(
        db,
        transaction_id
    )