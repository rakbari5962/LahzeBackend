from sqlalchemy.orm import Session

from app.models.financial_transaction import FinancialTransaction



def create_transaction(
    db: Session,
    transaction_id: str,
    transaction_type: str,
    total_amount: int,
    reference_type: str,
    reference_id: int,
    status: str = "PENDING"
):

    existing_transaction = db.query(
        FinancialTransaction
    ).filter(
        FinancialTransaction.transaction_id == transaction_id
    ).first()


    if existing_transaction:
        return existing_transaction



    transaction = FinancialTransaction(

        transaction_id=transaction_id,

        type=transaction_type,

        status=status,

        total_amount=total_amount,

        reference_type=reference_type,

        reference_id=reference_id

    )


    db.add(transaction)

    db.commit()

    db.refresh(transaction)


    return transaction





def get_transaction(
    db: Session,
    transaction_id: str
):

    return db.query(
        FinancialTransaction
    ).filter(
        FinancialTransaction.transaction_id == transaction_id
    ).first()





def get_transaction_by_reference(
    db: Session,
    reference_type: str,
    reference_id: int,
    transaction_type: str
):

    return db.query(
        FinancialTransaction
    ).filter(
        FinancialTransaction.reference_type == reference_type,
        FinancialTransaction.reference_id == reference_id,
        FinancialTransaction.type == transaction_type
    ).first()





def update_transaction_status(
    db: Session,
    transaction_id: str,
    status: str
):

    transaction = get_transaction(
        db,
        transaction_id
    )


    if not transaction:
        return None


    transaction.status = status


    db.commit()

    db.refresh(transaction)


    return transaction