from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.reward_event import RewardEvent
from app.models.booking import Booking
from app.models.opportunity import Opportunity

from app.services.account_service import (
    create_user_wallet_account,
    create_platform_treasury_account
)

from app.services.account_balance_service import (
    increase_account_balance,
    decrease_account_balance
)

from app.repositories.ledger_repository import (
    create_ledger_entry
)

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction,
    fail_financial_transaction,
    get_financial_transaction
)


# فعلاً زمان آزادسازی کمیسیون برای همه کسب‌وکارها 120 دقیقه است.
# بعداً می‌توان این مقدار را از تنظیمات هر Business خواند.
COMMISSION_RELEASE_DELAY_MINUTES = 120


def release_commission(
    db: Session,
    reward_event_id: int
):

    # --------------------------------------------------
    # 1. پیدا کردن کمیسیون PENDING
    # --------------------------------------------------

    reward_event = db.query(
        RewardEvent
    ).filter(
        RewardEvent.id == reward_event_id,
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).first()

    if not reward_event:
        return None


    # --------------------------------------------------
    # 2. Booking باید COMPLETED باشد
    # --------------------------------------------------

    booking = db.query(
        Booking
    ).filter(
        Booking.id == reward_event.booking_id,
        Booking.status == "COMPLETED"
    ).first()

    if not booking:
        return None


    # --------------------------------------------------
    # 3. پیدا کردن Opportunity
    # --------------------------------------------------

    opportunity = db.query(
        Opportunity
    ).filter(
        Opportunity.id == booking.opportunity_id
    ).first()

    if not opportunity:
        return None


    # --------------------------------------------------
    # 4. محاسبه زمان آزادسازی کمیسیون
    #
    # Release Time =
    # Opportunity.end_time + 120 minutes
    # --------------------------------------------------

    release_time = (
        opportunity.end_time
        +
        timedelta(
            minutes=COMMISSION_RELEASE_DELAY_MINUTES
        )
    )

    now = datetime.now(timezone.utc)

    if now < release_time:
        return None


    # --------------------------------------------------
    # 5. بررسی مبلغ کمیسیون
    # --------------------------------------------------

    amount = reward_event.amount

    if amount <= 0:
        return None


    # --------------------------------------------------
    # 6. حساب خزانه پلتفرم
    # --------------------------------------------------

    treasury_account = create_platform_treasury_account(
        db
    )

    if not treasury_account:
        return None


    # --------------------------------------------------
    # 7. کیف پول معرف
    # --------------------------------------------------

    user_wallet = create_user_wallet_account(
        db,
        reward_event.user_id
    )

    if not user_wallet:
        return None


    # --------------------------------------------------
    # 8. transaction_id ثابت و یکتا
    # برای هر RewardEvent فقط یک Release داریم
    # --------------------------------------------------

    transaction_id = (
        f"COMMISSION-RELEASE-{reward_event.id}"
    )


    # --------------------------------------------------
    # 9. جلوگیری از پرداخت دوباره
    # --------------------------------------------------

    existing_transaction = get_financial_transaction(
        db,
        transaction_id
    )

    if existing_transaction:

        # اگر قبلاً تراکنشی برای این کمیسیون ساخته شده باشد،
        # دوباره هیچ پولی جابه‌جا نمی‌کنیم.
        if existing_transaction.status in (
            "PENDING",
            "COMPLETED",
            "FAILED",
            "CANCELLED"
        ):
            return None


    # --------------------------------------------------
    # 10. ساخت FinancialTransaction
    # --------------------------------------------------

    financial_transaction = create_financial_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_type="COMMISSION_RELEASE",
        amount=amount,
        reference_type="REWARD_EVENT",
        reference_id=reward_event.id
    )

    if not financial_transaction:
        return None


    try:

        # --------------------------------------------------
        # 11. کم کردن کمیسیون از خزانه Lahze
        # --------------------------------------------------

        treasury_result = decrease_account_balance(
            db,
            treasury_account.id,
            amount
        )

        if not treasury_result:

            fail_financial_transaction(
                db,
                transaction_id
            )

            return None


        # --------------------------------------------------
        # 12. اضافه کردن کمیسیون به کیف پول معرف
        # --------------------------------------------------

        wallet_result = increase_account_balance(
            db,
            user_wallet.id,
            amount
        )

        if not wallet_result:

            fail_financial_transaction(
                db,
                transaction_id
            )

            return None


        # --------------------------------------------------
        # 13. Ledger خزانه پلتفرم
        # --------------------------------------------------

        create_ledger_entry(
            db=db,
            account_id=treasury_account.id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="DEBIT",
            amount=amount,
            reference_type="REWARD_EVENT",
            reference_id=reward_event.id
        )


        # --------------------------------------------------
        # 14. Ledger کیف پول معرف
        # --------------------------------------------------

        create_ledger_entry(
            db=db,
            account_id=user_wallet.id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="CREDIT",
            amount=amount,
            reference_type="REWARD_EVENT",
            reference_id=reward_event.id
        )


        # --------------------------------------------------
        # 15. تکمیل FinancialTransaction
        # --------------------------------------------------

        complete_financial_transaction(
            db,
            transaction_id
        )


        # --------------------------------------------------
        # 16. تکمیل RewardEvent
        # --------------------------------------------------

        reward_event.status = "PROCESSED"
        reward_event.transaction_id = transaction_id

        db.commit()
        db.refresh(reward_event)

        return reward_event


    except Exception:

        fail_financial_transaction(
            db,
            transaction_id
        )

        raise

    

def release_due_commissions(
    db: Session
):

    # --------------------------------------------------
    # پیدا کردن تمام کمیسیون‌های در انتظار
    # --------------------------------------------------

    pending_events = db.query(
        RewardEvent
    ).filter(
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).all()


    processed_event_ids = []


    # --------------------------------------------------
    # بررسی تک‌تک کمیسیون‌ها
    # --------------------------------------------------

    for reward_event in pending_events:

        result = release_commission(
            db=db,
            reward_event_id=reward_event.id
        )

        if result:

            processed_event_ids.append(
                result.id
            )


    # --------------------------------------------------
    # خروجی برای Scheduler / Log
    # --------------------------------------------------

    return {
        "checked": len(pending_events),
        "released": len(processed_event_ids),
        "released_event_ids": processed_event_ids
    }