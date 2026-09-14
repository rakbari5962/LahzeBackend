from sqlalchemy.orm import Session
import uuid

from app.services.wallet_service import get_or_create_user_wallet

from app.services.account_balance_service import (
    increase_account_balance,
    decrease_account_balance
)

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction
)

from app.repositories.ledger_repository import create_ledger_entry

from app.models.account import Account



def get_escrow_account(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "ESCROW"
    ).first()





def create_payment(
    db: Session,
    user_id: int,
    amount: int,
    booking_id: int
):

    if amount <= 0:
        return None


    # 1. کیف پول مشتری
    user_wallet = get_or_create_user_wallet(
        db,
        user_id
    )


    if not user_wallet:
        return None



    # 2. حساب Escrow
    escrow = get_escrow_account(
        db
    )


    if not escrow:
        return None



    # 3. بررسی موجودی
    if user_wallet.balance < amount:
        return None



    # 4. ساخت Transaction
    transaction_id = (
        "PAY-" +
        str(uuid.uuid4())
    )


    transaction = create_financial_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_type="PAYMENT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )


    if not transaction:
        return None



    # 5. Ledger خروج پول از مشتری

    debit_ledger = create_ledger_entry(
        db=db,
        account_id=user_wallet.id,
        transaction_id=transaction_id,
        entry_type="PAYMENT",
        direction="DEBIT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    # 6. Ledger ورود پول به Escrow

    credit_ledger = create_ledger_entry(
        db=db,
        account_id=escrow.id,
        transaction_id=transaction_id,
        entry_type="PAYMENT",
        direction="CREDIT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    # 7. تغییر موجودی مشتری

    decrease_account_balance(
        db,
        user_wallet.id,
        amount
    )


    # 8. افزایش Escrow

    increase_account_balance(
        db,
        escrow.id,
        amount
    )



    # 9. تکمیل تراکنش

    complete_financial_transaction(
        db,
        transaction_id
    )


    return {
        "transaction": transaction,
        "debit": debit_ledger,
        "credit": credit_ledger
    }