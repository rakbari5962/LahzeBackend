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

from app.repositories.ledger_repository import create_ledger_entry



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





def settle_payment(
    db: Session,
    booking_id: int,
    business_id: int,
    amount: int
):

    if amount <= 0:
        return None



    # جلوگیری از Settlement تکراری برای یک Booking

    existing_settlement = get_transaction_by_reference(
        db=db,
        reference_type="BOOKING",
        reference_id=booking_id,
        transaction_type="SETTLEMENT"
    )


    if existing_settlement:

        print(
            "DUPLICATE SETTLEMENT:",
            existing_settlement.transaction_id
        )


        return {
            "transaction": existing_settlement,
            "duplicate": True
        }



    escrow = get_escrow_account(db)


    business_account = get_business_account(
        db,
        business_id
    )


    treasury = get_platform_treasury_account(
        db
    )




    if not escrow:

        record_error(
            db=db,
            error_code=500,
            action="SETTLEMENT",
            context={
                "reason": "ESCROW_NOT_FOUND",
                "booking_id": booking_id,
                "business_id": business_id,
                "amount": amount
            }
        )

        return None




    if not business_account:

        record_error(
            db=db,
            error_code=500,
            action="SETTLEMENT",
            context={
                "reason": "BUSINESS_ACCOUNT_NOT_FOUND",
                "booking_id": booking_id,
                "business_id": business_id,
                "amount": amount
            }
        )

        return None




    if not treasury:

        record_error(
            db=db,
            error_code=500,
            action="SETTLEMENT",
            context={
                "reason": "TREASURY_NOT_FOUND",
                "booking_id": booking_id,
                "business_id": business_id,
                "amount": amount
            }
        )

        return None





    if escrow.balance < amount:

        record_error(
            db=db,
            error_code=500,
            action="SETTLEMENT",
            context={
                "reason": "ESCROW_LOW_BALANCE",
                "booking_id": booking_id,
                "business_id": business_id,
                "escrow_balance": escrow.balance,
                "required_amount": amount
            }
        )

        return None





    business_amount = int(
        amount * 0.95
    )


    platform_amount = (
        amount - business_amount
    )




    transaction_id = (
        "SETTLE-" +
        str(uuid.uuid4())
    )




    transaction = create_financial_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_type="SETTLEMENT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )




    if not transaction:

        record_error(
            db=db,
            error_code=500,
            action="SETTLEMENT",
            context={
                "reason": "TRANSACTION_CREATION_FAILED",
                "booking_id": booking_id,
                "business_id": business_id,
                "amount": amount
            }
        )

        return None





    # ESCROW خروج کل مبلغ

    create_ledger_entry(
        db=db,
        account_id=escrow.id,
        transaction_id=transaction_id,
        entry_type="SETTLEMENT",
        direction="DEBIT",
        amount=amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )




    # سهم کسب و کار

    create_ledger_entry(
        db=db,
        account_id=business_account.id,
        transaction_id=transaction_id,
        entry_type="SETTLEMENT",
        direction="CREDIT",
        amount=business_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )




    # سهم پلتفرم

    create_ledger_entry(
        db=db,
        account_id=treasury.id,
        transaction_id=transaction_id,
        entry_type="SETTLEMENT",
        direction="CREDIT",
        amount=platform_amount,
        reference_type="BOOKING",
        reference_id=booking_id
    )




    decrease_account_balance(
        db,
        escrow.id,
        amount
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
        transaction_id
    )




    print(
        "SETTLEMENT COMPLETED"
    )

    print(
        "Platform Amount:",
        platform_amount
    )




    trigger_settlement_rewards(
        db=db,
        business_id=business_id,
        platform_amount=platform_amount,
        settlement_reference_id=booking_id
    )

    trigger_priority_access_rewards(
        db=db,
        business_id=business_id,
        booking_id=booking_id,
        amount=amount
    )



    return {
        "transaction": transaction,
        "business_amount": business_amount,
        "platform_amount": platform_amount
    }