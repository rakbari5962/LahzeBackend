from sqlalchemy.orm import Session
import uuid

from app.services.wallet_service import get_or_create_user_wallet

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction
)

from app.services.account_balance_service import (
    increase_account_balance
)

from app.repositories.ledger_repository import (
    create_ledger_entry
)


def deposit_to_user_wallet(
    db: Session,
    user_id: int,
    amount: int,
    transaction_type: str = "DEPOSIT",
    reference_type: str = "USER_WALLET"
):

    if amount <= 0:
        return None


    # 1. پیدا کردن یا ساخت کیف پول کاربر

    wallet = get_or_create_user_wallet(
        db,
        user_id
    )


    if not wallet:
        return None



    # 2. ساخت شناسه تراکنش

    transaction_id = (
        "DEP-" +
        str(uuid.uuid4())
    )



    # 3. ایجاد Financial Transaction

    transaction = create_financial_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_type=transaction_type,
        amount=amount,
        reference_type=reference_type,
        reference_id=user_id
    )


    if not transaction:
        return None



    # 4. ثبت Ledger Entry

    ledger = create_ledger_entry(
        db=db,
        account_id=wallet.id,
        transaction_id=transaction_id,
        entry_type=transaction_type,
        direction="CREDIT",
        amount=amount,
        reference_type=reference_type,
        reference_id=user_id
    )


    if not ledger:
        return None



    # 5. افزایش موجودی کیف پول

    updated_wallet = increase_account_balance(
        db,
        wallet.id,
        amount
    )


    if not updated_wallet:
        return None



    # 6. تکمیل تراکنش

    complete_financial_transaction(
        db,
        transaction_id
    )


    return {
        "transaction": transaction,
        "wallet": updated_wallet,
        "ledger": ledger
    }