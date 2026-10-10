from datetime import datetime, timezone, timedelta

from sqlalchemy.exc import IntegrityError
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

    # ???? ????????? ?? ???? SQLite? ???? ??? datetime ??
    # ???? timezone ?????????. ???????? ????????? ?? UTC ??? ???????.
    if release_time.tzinfo is None:
        release_time = release_time.replace(tzinfo=timezone.utc)
    else:
        release_time = release_time.astimezone(timezone.utc)

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
    # 6. Lock the pending reward event before financial side effects.
    # --------------------------------------------------

    locked_reward_event = db.query(
        RewardEvent
    ).filter(
        RewardEvent.id == reward_event_id,
        RewardEvent.type == "REFERRAL_COMMISSION",
        RewardEvent.status == "PENDING"
    ).with_for_update().first()

    if not locked_reward_event:
        db.rollback()
        return None

    reward_event = locked_reward_event

    transaction_id = (
        f"COMMISSION-RELEASE-{reward_event.id}"
    )

    existing_transaction = get_financial_transaction(
        db,
        transaction_id
    )

    if existing_transaction:
        db.rollback()
        return None


    # --------------------------------------------------
    # 7. حساب خزانه پلتفرم
    # --------------------------------------------------

    try:
        treasury_account = create_platform_treasury_account(
            db,
            commit=False,
        )
    except IntegrityError:
        db.rollback()
        return None

    if not treasury_account:
        db.rollback()
        return None


    # --------------------------------------------------
    # 8. کیف پول معرف
    # --------------------------------------------------

    try:
        user_wallet = create_user_wallet_account(
            db,
            reward_event.user_id,
            commit=False,
        )
    except IntegrityError:
        db.rollback()
        return None

    if not user_wallet:
        db.rollback()
        return None


    # --------------------------------------------------
    # 9. ساخت FinancialTransaction
    # --------------------------------------------------

    try:
        # ??? ??????? ???? ?? ????? ?????? ?? ?? ?????? ???? ????????.
        try:
            financial_transaction = create_financial_transaction(
                db=db,
                transaction_id=transaction_id,
                transaction_type="COMMISSION_RELEASE",
                amount=amount,
                reference_type="REWARD_EVENT",
                reference_id=reward_event.id,
                commit=False,
                fail_if_exists=True,
            )
        except IntegrityError:
            # A concurrent request may have inserted this unique ID.
            db.rollback()
            return None

        if not financial_transaction:
            db.rollback()
            return None

        # Guard against reusing an existing transaction.
        # Only a matching PENDING transaction may proceed.
        if (
            financial_transaction.transaction_id != transaction_id
            or financial_transaction.type != "COMMISSION_RELEASE"
            or financial_transaction.status != "PENDING"
            or financial_transaction.total_amount != amount
            or financial_transaction.reference_type != "REWARD_EVENT"
            or financial_transaction.reference_id != reward_event.id
        ):
            db.rollback()
            return None

        treasury_result = decrease_account_balance(
            db,
            treasury_account.id,
            amount,
            commit=False,
        )

        if not treasury_result:
            db.rollback()
            return None

        wallet_result = increase_account_balance(
            db,
            user_wallet.id,
            amount,
            commit=False,
        )

        if not wallet_result:
            db.rollback()
            return None

        debit_entry = create_ledger_entry(
            db=db,
            account_id=treasury_account.id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="DEBIT",
            amount=amount,
            reference_type="REWARD_EVENT",
            reference_id=reward_event.id,
            commit=False,
        )

        if not debit_entry:
            db.rollback()
            return None

        credit_entry = create_ledger_entry(
            db=db,
            account_id=user_wallet.id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="CREDIT",
            amount=amount,
            reference_type="REWARD_EVENT",
            reference_id=reward_event.id,
            commit=False,
        )

        if not credit_entry:
            db.rollback()
            return None

        completed_transaction = complete_financial_transaction(
            db,
            transaction_id,
            commit=False,
        )

        if not completed_transaction:
            db.rollback()
            return None

        reward_event.status = "PROCESSED"
        reward_event.transaction_id = transaction_id

        # ???? ???? ??? ????? ?????? ???????
        db.commit()
        db.refresh(reward_event)

        return reward_event

    except Exception:
        db.rollback()
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