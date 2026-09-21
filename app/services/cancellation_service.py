from app.services.settlement_reward_trigger_service import (
    trigger_settlement_rewards
)

from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid

from app.models.account import Account
from app.models.booking import Booking
from app.models.business import Business
from app.models.user import User
from app.models.opportunity import Opportunity

from app.schemas.notification import NotificationCreate

from app.repositories.notification_repository import (
    create_notification
)

from app.services.sms_service import (
    send_booking_cancellation_notification
)

from app.services.account_balance_service import (
    increase_account_balance,
    decrease_account_balance
)

from app.services.financial_transaction_service import (
    create_financial_transaction,
    complete_financial_transaction
)

from app.repositories.ledger_repository import (
    create_ledger_entry
)



def get_escrow_account(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "ESCROW"
    ).first()



def get_customer_wallet(
    db: Session,
    user_id: int
):

    return db.query(Account).filter(
        Account.owner_type == "USER",
        Account.owner_id == user_id,
        Account.account_type == "CUSTOMER_WALLET"
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



def get_platform_treasury(
    db: Session
):

    return db.query(Account).filter(
        Account.owner_type == "PLATFORM",
        Account.account_type == "PLATFORM_TREASURY"
    ).first()





def cancel_confirmed_booking(
    db: Session,
    booking_id: int,
    amount: int
    ):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None


    if booking.status != "CONFIRMED":
        return None



    escrow = get_escrow_account(db)


    customer_wallet = get_customer_wallet(
        db,
        booking.user_id
    )


    business_account = get_business_account(
        db,
        booking.business_id
    )


    treasury = get_platform_treasury(
        db
    )



    if (
        not escrow
        or not customer_wallet
        or not business_account
        or not treasury
    ):
        return None



    if escrow.balance < amount:
        return None



    customer_amount = int(
        amount * 0.70
    )


    business_amount = int(
        amount * 0.25
    )


    platform_amount = (
        amount
        -
        customer_amount
        -
        business_amount
    )



    # -----------------------------
    # Customer Refund Transaction
    # -----------------------------

    refund_transaction_id = (
        "CUSTOMER-REFUND-"
        +
        str(uuid.uuid4())
    )


    refund_transaction = create_financial_transaction(
        db=db,
        transaction_id=refund_transaction_id,
        transaction_type="CUSTOMER_REFUND",
        amount=customer_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )


    if not refund_transaction:
        return None



    # -----------------------------
    # Business Fee Transaction
    # -----------------------------

    business_transaction_id = (
        "BUSINESS-FEE-"
        +
        str(uuid.uuid4())
    )


    create_financial_transaction(
        db=db,
        transaction_id=business_transaction_id,
        transaction_type="CANCELLATION_FEE_BUSINESS",
        amount=business_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    # -----------------------------
    # Platform Fee Transaction
    # -----------------------------

    platform_transaction_id = (
        "PLATFORM-FEE-"
        +
        str(uuid.uuid4())
    )


    create_financial_transaction(
        db=db,
        transaction_id=platform_transaction_id,
        transaction_type="CANCELLATION_FEE_PLATFORM",
        amount=platform_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )

    # -----------------------------
    # Ledger
    # -----------------------------


    create_ledger_entry(
        db=db,
        account_id=escrow.id,
        transaction_id=refund_transaction_id,
        entry_type="REFUND",
        direction="DEBIT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    create_ledger_entry(
        db=db,
        account_id=customer_wallet.id,
        transaction_id=refund_transaction_id,
        entry_type="REFUND",
        direction="CREDIT",
        amount=customer_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    create_ledger_entry(
        db=db,
        account_id=business_account.id,
        transaction_id=business_transaction_id,
        entry_type="CANCELLATION_FEE",
        direction="CREDIT",
        amount=business_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    create_ledger_entry(
        db=db,
        account_id=treasury.id,
        transaction_id=platform_transaction_id,
        entry_type="CANCELLATION_FEE",
        direction="CREDIT",
        amount=platform_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )



    # -----------------------------
    # Balance Update
    # -----------------------------

    decrease_account_balance(
        db,
        escrow.id,
        amount
    )


    increase_account_balance(
        db,
        customer_wallet.id,
        customer_amount
    )


    increase_account_balance(
        db,
        business_account.id,
        business_amount
    )


    increase_account_balance(
        db,
        treasury.id,
        platform_amount
    )



    complete_financial_transaction(
        db,
        refund_transaction_id
    )


    complete_financial_transaction(
        db,
        business_transaction_id
    )


    complete_financial_transaction(
        db,
        platform_transaction_id
    )

    trigger_settlement_rewards(
        db=db,
        business_id=booking.business_id,
        platform_amount=platform_amount,
        settlement_reference_id=booking_id
    )

    opportunity = db.query(Opportunity).filter(
        Opportunity.id == booking.opportunity_id
    ).first()


    if opportunity:

        if opportunity.reserved_count > 0:

            opportunity.reserved_count -= 1


        if opportunity.reserved_count < opportunity.capacity:

            opportunity.status = "ACTIVE"



    booking.status = "CANCELLED"

    booking.cancelled_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(booking)



    # -----------------------------
    # Notification + SMS
    # -----------------------------

    business = db.query(Business).filter(
        Business.id == booking.business_id
    ).first()



    if business:

        owner = db.query(User).filter(
            User.id == business.owner_user_id
        ).first()


        if owner:

            notification = NotificationCreate(
                user_id=owner.id,
                type="BOOKING_CANCELLED",
                title="لغو رزرو توسط مشتری",
                message=(
                    f"رزرو شماره {booking.id} لغو شد. "
                    f"مبلغ {business_amount} ریال "
                    "به کیف پول شما اضافه شد."
                )
            )


            create_notification(
                db,
                notification
            )



            try:

                send_booking_cancellation_notification(
                    mobile=owner.phone_number,
                    business_name=business.name,
                    booking_id=booking.id,
                    penalty_amount=business_amount
                )


            except Exception as e:

                print(
                    "BOOKING CANCEL SMS ERROR:",
                    repr(e)
                )



    return booking


def cancel_pending_booking(
        db: Session,
        booking_id: int
    ):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        return None

    if booking.status != "PENDING_CONFIRMATION":
        return None

    booking.status = "CANCELLED"

    booking.cancelled_at = datetime.now(
        timezone.utc
    )

    db.commit()
    db.refresh(booking)

    return booking


def preview_cancel_confirmed_booking(
    db: Session,
    booking_id: int,
    amount: int
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()


    if not booking:
        return None


    if booking.status != "CONFIRMED":
        return None



    penalty_percent = 30


    penalty_amount = int(
        amount * 0.30
    )


    customer_refund = (
        amount - penalty_amount
    )


    return {
        "booking_id": booking.id,
        "amount": amount,
        "penalty_percent": penalty_percent,
        "penalty_amount": penalty_amount,
        "customer_refund": customer_refund,
        "requires_confirmation": True
    }