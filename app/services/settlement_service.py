from app.services.priority_access_reward_service import (
    trigger_priority_access_rewards
)

from app.repositories.financial_transaction_repository import (
    get_transaction_by_reference
)

from app.services.settlement_reward_trigger_service import (
    trigger_settlement_rewards
)

from app.services.error_service import (
    record_error
)

from sqlalchemy.orm import Session
import uuid

from app.models.account import Account

from app.services.account_balance_service import (
    increase_account_balance,
    decrease_account_balance
)

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction
)

from app.repositories.ledger_repository import (
    create_ledger_entry,
    get_transaction_entries,
)



def get_escrow_account(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "ESCROW"
    ).first()



def get_business_account(
    db: Session,
    business_id: int
):

    return db.query(Account).filter(
        Account.owner_type == "BUSINESS",
        Account.owner_id == business_id,
        Account.account_type == "BUSINESS_REVENUE"
    ).first()



def get_platform_treasury_account(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "PLATFORM_TREASURY"
    ).first()





def _validated_existing_settlement(
    db: Session,
    transaction,
    booking_id: int,
    amount: int,
):
    # تراکنش موجود فقط در صورت تکمیل و اعتبارسنجی
    # اسناد حسابداری، تسویه موفق محسوب می‌شود.
    if (
        transaction.type != "SETTLEMENT"
        or transaction.status != "COMPLETED"
        or transaction.total_amount != amount
        or transaction.reference_type != "BOOKING"
        or transaction.reference_id != booking_id
    ):
        print(
            "SETTLEMENT REQUIRES RECONCILIATION:",
            transaction.transaction_id,
            transaction.status,
        )
        return None

    entries = get_transaction_entries(
        db,
        transaction.transaction_id,
    )

    if len(entries) != 3:
        print(
            "SETTLEMENT LEDGER COUNT INVALID:",
            transaction.transaction_id,
        )
        return None

    debits = [
        entry for entry in entries
        if entry.direction == "DEBIT"
    ]

    credits = [
        entry for entry in entries
        if entry.direction == "CREDIT"
    ]

    if len(debits) != 1 or len(credits) != 2:
        return None

    for entry in entries:
        if (
            entry.entry_type != "SETTLEMENT"
            or entry.reference_type != "BOOKING"
            or entry.reference_id != booking_id
        ):
            return None

    business_amount = int(amount * 0.95)
    platform_amount = amount - business_amount

    if debits[0].amount != amount:
        return None

    if sorted(entry.amount for entry in credits) != sorted(
        [business_amount, platform_amount]
    ):
        return None

    return {
        "transaction": transaction,
        "business_amount": business_amount,
        "platform_amount": platform_amount,
        "duplicate": True,
    }


def settle_payment(
    db: Session,
    booking_id: int,
    business_id: int,
    amount: int,
):
    if amount <= 0 or booking_id <= 0 or business_id <= 0:
        return None

    try:
        # 1. بررسی تسویه قبلی
        existing_settlement = get_transaction_by_reference(
            db=db,
            reference_type="BOOKING",
            reference_id=booking_id,
            transaction_type="SETTLEMENT",
        )

        if existing_settlement:
            return _validated_existing_settlement(
                db,
                existing_settlement,
                booking_id,
                amount,
            )

        # 2. دریافت حساب‌ها
        escrow = get_escrow_account(db)
        business_account = get_business_account(
            db,
            business_id,
        )
        treasury = get_platform_treasury_account(db)

        if not escrow or not business_account or not treasury:
            record_error(
                db=db,
                error_code=500,
                action="SETTLEMENT",
                context={
                    "reason": "SETTLEMENT_ACCOUNT_NOT_FOUND",
                    "booking_id": booking_id,
                    "business_id": business_id,
                    "amount": amount,
                },
            )
            return None

        # 3. قفل حساب‌ها با ترتیب ثابت
        escrow_id = escrow.id
        business_account_id = business_account.id
        treasury_id = treasury.id

        account_ids = sorted({
            escrow_id,
            business_account_id,
            treasury_id,
        })

        account_model = type(escrow)

        locked_accounts = (
            db.query(account_model)
            .filter(account_model.id.in_(account_ids))
            .order_by(account_model.id)
            .with_for_update()
            .all()
        )

        locked_by_id = {
            account.id: account
            for account in locked_accounts
        }

        escrow = locked_by_id.get(escrow_id)
        business_account = locked_by_id.get(
            business_account_id
        )
        treasury = locked_by_id.get(treasury_id)

        if not escrow or not business_account or not treasury:
            db.rollback()
            return None

        # 4. بررسی مجدد بعد از قفل حساب‌ها
        existing_settlement = get_transaction_by_reference(
            db=db,
            reference_type="BOOKING",
            reference_id=booking_id,
            transaction_type="SETTLEMENT",
        )

        if existing_settlement:
            db.rollback()
            return _validated_existing_settlement(
                db,
                existing_settlement,
                booking_id,
                amount,
            )

        # 5. بررسی موجودی حساب امانی
        if escrow.balance < amount:
            current_balance = escrow.balance
            db.rollback()

            record_error(
                db=db,
                error_code=500,
                action="SETTLEMENT",
                context={
                    "reason": "ESCROW_LOW_BALANCE",
                    "booking_id": booking_id,
                    "business_id": business_id,
                    "escrow_balance": current_balance,
                    "required_amount": amount,
                },
            )
            return None

        business_amount = int(amount * 0.95)
        platform_amount = amount - business_amount

        transaction_id = "SETTLE-" + str(uuid.uuid4())

        # 6. ایجاد تراکنش بدون Commit مستقل
        transaction = create_financial_transaction(
            db=db,
            transaction_id=transaction_id,
            transaction_type="SETTLEMENT",
            amount=amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if (
            not transaction
            or transaction.transaction_id != transaction_id
            or transaction.type != "SETTLEMENT"
            or transaction.reference_type != "BOOKING"
            or transaction.reference_id != booking_id
            or transaction.status != "PENDING"
        ):
            db.rollback()
            return None

        # 7. بدهکار کردن حساب امانی
        debit_entry = create_ledger_entry(
            db=db,
            account_id=escrow.id,
            transaction_id=transaction_id,
            entry_type="SETTLEMENT",
            direction="DEBIT",
            amount=amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not debit_entry:
            db.rollback()
            return None

        # 8. بستانکار کردن حساب کسب‌وکار
        business_entry = create_ledger_entry(
            db=db,
            account_id=business_account.id,
            transaction_id=transaction_id,
            entry_type="SETTLEMENT",
            direction="CREDIT",
            amount=business_amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not business_entry:
            db.rollback()
            return None

        # 9. بستانکار کردن خزانه پلتفرم
        platform_entry = create_ledger_entry(
            db=db,
            account_id=treasury.id,
            transaction_id=transaction_id,
            entry_type="SETTLEMENT",
            direction="CREDIT",
            amount=platform_amount,
            reference_type="BOOKING",
            reference_id=booking_id,
            commit=False,
        )

        if not platform_entry:
            db.rollback()
            return None

        # 10. تغییر موجودی‌ها، بدون Commit مستقل
        debited = decrease_account_balance(
            db,
            escrow.id,
            amount,
            commit=False,
        )

        if not debited:
            db.rollback()
            return None

        business_credited = increase_account_balance(
            db,
            business_account.id,
            business_amount,
            commit=False,
        )

        if not business_credited:
            db.rollback()
            return None

        platform_credited = increase_account_balance(
            db,
            treasury.id,
            platform_amount,
            commit=False,
        )

        if not platform_credited:
            db.rollback()
            return None

        # 11. تکمیل تراکنش، همچنان در همان تراکنش DB
        completed_transaction = complete_financial_transaction(
            db,
            transaction_id,
            commit=False,
        )

        if (
            not completed_transaction
            or completed_transaction.status != "COMPLETED"
        ):
            db.rollback()
            return None

        # 12. تنها Commit عملیات اصلی تسویه
        db.commit()

    except Exception:
        db.rollback()
        raise

    # 13. پاداش‌ها پس از ثبت قطعی تسویه
    # خطای پاداش نباید تسویه ثبت‌شده را ناموفق جلوه دهد.
    try:
        trigger_settlement_rewards(
            db=db,
            business_id=business_id,
            platform_amount=platform_amount,
            settlement_reference_id=booking_id,
        )
    except Exception as reward_error:
        print(
            "SETTLEMENT REWARD ERROR:",
            repr(reward_error),
        )

    try:
        trigger_priority_access_rewards(
            db=db,
            business_id=business_id,
            booking_id=booking_id,
            amount=amount,
        )
    except Exception as reward_error:
        print(
            "PRIORITY REWARD ERROR:",
            repr(reward_error),
        )

    return {
        "transaction": completed_transaction,
        "business_amount": business_amount,
        "platform_amount": platform_amount,
        "duplicate": False,
    }