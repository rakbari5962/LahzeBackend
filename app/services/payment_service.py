from sqlalchemy.orm import Session

from app.services.account_balance_service import (
    increase_account_balance,
    decrease_account_balance,
)

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction,
)

from app.repositories.financial_transaction_repository import (
    get_transaction_by_reference,
)

from app.repositories.ledger_repository import (
    create_ledger_entry,
    get_transaction_entries,
)

from app.models.account import Account


def get_escrow_account(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "ESCROW"
    ).first()


def _completed_payment_result(
    db: Session,
    transaction,
    amount: int,
    booking_id: int,
    user_id: int,
):
    # Validate the transaction identity and final state.
    if (
        transaction.transaction_id != f"PAY-{booking_id}"
        or transaction.type != "PAYMENT"
        or transaction.reference_type != "BOOKING"
        or transaction.reference_id != booking_id
        or transaction.status != "COMPLETED"
        or transaction.total_amount != amount
        or amount <= 0
    ):
        return None

    entries = get_transaction_entries(
        db,
        transaction.transaction_id,
    )

    if len(entries) != 2:
        return None

    debit_entries = [
        entry for entry in entries
        if entry.direction == "DEBIT"
    ]
    credit_entries = [
        entry for entry in entries
        if entry.direction == "CREDIT"
    ]

    if len(debit_entries) != 1 or len(credit_entries) != 1:
        return None

    debit = debit_entries[0]
    credit = credit_entries[0]

    for entry in (debit, credit):
        if (
            entry.amount != amount
            or entry.entry_type != "PAYMENT"
            or entry.reference_type != "BOOKING"
            or entry.reference_id != booking_id
        ):
            return None

    # Verify that the debit belongs to this customer's wallet
    # and the credit belongs to the platform escrow account.
    user_wallet = db.query(Account).filter(
        Account.owner_type == "USER",
        Account.owner_id == user_id,
        Account.account_type == "CUSTOMER_WALLET",
    ).first()

    escrow = get_escrow_account(db)

    if not user_wallet or not escrow:
        return None

    if (
        debit.account_id != user_wallet.id
        or credit.account_id != escrow.id
    ):
        return None

    return {
        "transaction": transaction,
        "debit": debit,
        "credit": credit,
    }


def validate_completed_payment(
    db: Session,
    user_id: int,
    amount: int,
    booking_id: int,
):
    # Read-only validation for an already-confirmed booking.
    if amount <= 0 or booking_id <= 0:
        return None

    transaction = get_transaction_by_reference(
        db,
        reference_type="BOOKING",
        reference_id=booking_id,
        transaction_type="PAYMENT",
    )

    if not transaction:
        return None

    return _completed_payment_result(
        db=db,
        transaction=transaction,
        amount=amount,
        booking_id=booking_id,
        user_id=user_id,
    )


def create_payment(
    db: Session,
    user_id: int,
    amount: int,
    booking_id: int,
    commit: bool = True,
):
    if amount <= 0 or booking_id <= 0:
        return None

    try:
        # 1. بررسی پرداخت قبلی این رزرو
        existing = get_transaction_by_reference(
            db,
            reference_type="BOOKING",
            reference_id=booking_id,
            transaction_type="PAYMENT",
        )

        if existing:
            return _completed_payment_result(
                db,
                existing,
                amount,
                booking_id,
                user_id=user_id,
            )

        # 2. دریافت کیف پول موجود مشتری؛
        # در صورت نبود کیف پول، آن را بی‌دلیل ایجاد نکن.
        user_wallet = db.query(Account).filter(
            Account.owner_type == "USER",
            Account.owner_id == user_id,
            Account.account_type == "CUSTOMER_WALLET",
        ).first()

        escrow = get_escrow_account(db)

        if not user_wallet or not escrow:
            return None

        # 3. قفل کردن حساب‌ها با ترتیب ثابت برای کاهش
        # احتمال تداخل پرداخت‌های هم‌زمان.
        account_ids = sorted({
            user_wallet.id,
            escrow.id,
        })

        locked_accounts = (
            db.query(Account)
            .filter(Account.id.in_(account_ids))
            .order_by(Account.id)
            .with_for_update()
            .all()
        )

        locked_by_id = {
            account.id: account
            for account in locked_accounts
        }

        user_wallet = locked_by_id.get(user_wallet.id)
        escrow = locked_by_id.get(escrow.id)

        if not user_wallet or not escrow:
            db.rollback()
            return None

        # 4. بررسی مجدد پرداخت پس از قفل حساب‌ها
        # تا درخواست‌های هم‌زمان یک رزرو دوباره پرداخت نکنند.
        existing = get_transaction_by_reference(
            db,
            reference_type="BOOKING",
            reference_id=booking_id,
            transaction_type="PAYMENT",
        )

        if existing:
            return _completed_payment_result(
                db,
                existing,
                amount,
                booking_id,
                user_id=user_id,
            )


        # 5. بررسی موجودی پس از گرفتن قفل حساب
        if user_wallet.balance < amount:
            db.rollback()
            return None

        # 6. شناسه ثابت برای هر رزرو
        transaction_id = f"PAY-{booking_id}"

        transaction = create_financial_transaction(
            db=db,
            transaction_id=transaction_id,
            transaction_type="PAYMENT",
            amount=amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not transaction:
            db.rollback()
            return None

        # از استفاده تصادفی از یک شناسه برای تراکنش
        # نامرتبط جلوگیری کن.
        if (
            transaction.transaction_id != transaction_id
            or transaction.type != "PAYMENT"
            or transaction.reference_type != "BOOKING"
            or transaction.reference_id != booking_id
            or transaction.status != "PENDING"
        ):
            db.rollback()
            return None

        # 7. سند بدهکار کیف پول مشتری
        debit_ledger = create_ledger_entry(
            db=db,
            account_id=user_wallet.id,
            transaction_id=transaction_id,
            entry_type="PAYMENT",
            direction="DEBIT",
            amount=amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not debit_ledger:
            db.rollback()
            return None

        # 8. سند بستانکار حساب امانی
        credit_ledger = create_ledger_entry(
            db=db,
            account_id=escrow.id,
            transaction_id=transaction_id,
            entry_type="PAYMENT",
            direction="CREDIT",
            amount=amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not credit_ledger:
            db.rollback()
            return None

        # 9. کاهش موجودی کیف پول مشتری
        debited_account = decrease_account_balance(
            db,
            user_wallet.id,
            amount,
            commit=False,
        )

        if not debited_account:
            db.rollback()
            return None

        # 10. افزایش موجودی حساب امانی
        credited_account = increase_account_balance(
            db,
            escrow.id,
            amount,
            commit=False,
        )

        if not credited_account:
            db.rollback()
            return None

        # 11. تکمیل تراکنش، بدون commit مستقل
        completed_transaction = complete_financial_transaction(
            db,
            transaction_id,
            commit=False,
        )

        if not completed_transaction:
            db.rollback()
            return None

        # 12. تنها نقطه ثبت نهایی عملیات پرداخت
        if commit:
            db.commit()
        else:
            db.flush()

        return {
            "transaction": completed_transaction,
            "debit": debit_ledger,
            "credit": credit_ledger,
        }

    except Exception:
        db.rollback()
        raise
