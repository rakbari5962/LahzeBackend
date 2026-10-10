from datetime import datetime, timedelta, timezone

import app.models
import app.services.commission_release_service as commission_release_service

from app.models.account import Account
from app.models.booking import Booking
from app.models.business import Business
from app.models.financial_transaction import FinancialTransaction
from app.models.ledger import LedgerEntry
from app.models.opportunity import Opportunity
from app.models.reward_event import RewardEvent
from app.models.service import Service
from app.models.user import User


def test_commission_release_failure_rolls_back_every_financial_change(
    db,
    monkeypatch,
):
    owner = User(
        phone_number="09129991001",
        role="CUSTOMER",
        profile_completed=True,
    )
    referrer = User(
        phone_number="09129991002",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09129991003",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, referrer, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Commission Atomicity Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Commission Test Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    end_time = datetime.now(timezone.utc) - timedelta(hours=4)
    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=end_time - timedelta(hours=1),
        end_time=end_time,
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=1,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status="COMPLETED",
    )
    db.add(booking)
    db.flush()

    reward_event = RewardEvent(
        user_id=referrer.id,
        business_id=business.id,
        booking_id=booking.id,
        idempotency_key="TEST-COMMISSION-ATOMICITY-001",
        type="REFERRAL_COMMISSION",
        amount=1000,
        status="PENDING",
    )

    treasury = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    wallet = Account(
        owner_type="USER",
        owner_id=referrer.id,
        account_type="CUSTOMER_WALLET",
        balance=250,
        currency="IRR",
        status="ACTIVE",
    )
    db.add_all([reward_event, treasury, wallet])
    db.flush()

    reward_event_id = reward_event.id
    treasury_id = treasury.id
    wallet_id = wallet.id
    transaction_id = f"COMMISSION-RELEASE-{reward_event_id}"

    # Establish committed fixture state before testing rollback.
    # This keeps the test setup separate from the operation under test.
    db.commit()

    # Simulate failure when crediting the referrer's wallet.
    monkeypatch.setattr(
        commission_release_service,
        "increase_account_balance",
        lambda *args, **kwargs: None,
    )

    result = commission_release_service.release_commission(
        db,
        reward_event_id,
    )

    assert result is None

    db.expire_all()

    actual = {
        "treasury_balance": (
            db.query(Account).filter(Account.id == treasury_id).one().balance
        ),
        "wallet_balance": (
            db.query(Account).filter(Account.id == wallet_id).one().balance
        ),
        "financial_transaction_count": (
            db.query(FinancialTransaction)
            .filter(
                FinancialTransaction.transaction_id == transaction_id
            )
            .count()
        ),
        "ledger_entry_count": (
            db.query(LedgerEntry)
            .filter(LedgerEntry.transaction_id == transaction_id)
            .count()
        ),
        "reward_event_status": (
            db.query(RewardEvent)
            .filter(RewardEvent.id == reward_event_id)
            .one()
            .status
        ),
    }

    expected = {
        "treasury_balance": 5000,
        "wallet_balance": 250,
        "financial_transaction_count": 0,
        "ledger_entry_count": 0,
        "reward_event_status": "PENDING",
    }

    assert actual == expected


def test_commission_release_success_and_retry_does_not_transfer_twice(db):
    from app.models.financial_transaction import FinancialTransaction
    from app.models.ledger import LedgerEntry

    owner = User(
        phone_number="09129991011",
        role="CUSTOMER",
        profile_completed=True,
    )
    referrer = User(
        phone_number="09129991012",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09129991013",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, referrer, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Commission Success Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Commission Success Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    end_time = datetime.now(timezone.utc) - timedelta(hours=4)
    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=end_time - timedelta(hours=1),
        end_time=end_time,
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=1,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status="COMPLETED",
    )
    db.add(booking)
    db.flush()

    reward_event = RewardEvent(
        user_id=referrer.id,
        business_id=business.id,
        booking_id=booking.id,
        idempotency_key="TEST-COMMISSION-SUCCESS-001",
        type="REFERRAL_COMMISSION",
        amount=1000,
        status="PENDING",
    )

    treasury = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    wallet = Account(
        owner_type="USER",
        owner_id=referrer.id,
        account_type="CUSTOMER_WALLET",
        balance=250,
        currency="IRR",
        status="ACTIVE",
    )
    db.add_all([reward_event, treasury, wallet])
    db.flush()

    reward_event_id = reward_event.id
    treasury_id = treasury.id
    wallet_id = wallet.id
    transaction_id = f"COMMISSION-RELEASE-{reward_event_id}"

    # Commit baseline fixtures before testing the service transaction.
    db.commit()

    result = commission_release_service.release_commission(
        db,
        reward_event_id,
    )

    assert result is not None
    assert result.status == "PROCESSED"
    assert result.transaction_id == transaction_id

    db.refresh(treasury)
    db.refresh(wallet)

    assert treasury.id == treasury_id
    assert wallet.id == wallet_id
    assert treasury.balance == 4000
    assert wallet.balance == 1250

    transactions = (
        db.query(FinancialTransaction)
        .filter(
            FinancialTransaction.transaction_id == transaction_id
        )
        .all()
    )
    assert len(transactions) == 1

    transaction = transactions[0]
    assert transaction.status == "COMPLETED"
    assert transaction.total_amount == 1000
    assert transaction.type == "COMMISSION_RELEASE"

    entries = (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .all()
    )

    assert len(entries) == 2
    assert {entry.direction for entry in entries} == {"DEBIT", "CREDIT"}
    assert all(entry.amount == 1000 for entry in entries)
    assert sum(
        entry.amount for entry in entries
        if entry.direction == "DEBIT"
    ) == 1000
    assert sum(
        entry.amount for entry in entries
        if entry.direction == "CREDIT"
    ) == 1000

    # A second release attempt must not transfer funds again.
    retry = commission_release_service.release_commission(
        db,
        reward_event_id,
    )
    assert retry is None

    db.refresh(treasury)
    db.refresh(wallet)
    db.refresh(reward_event)

    assert treasury.balance == 4000
    assert wallet.balance == 1250
    assert reward_event.status == "PROCESSED"
    assert reward_event.transaction_id == transaction_id

    assert (
        db.query(FinancialTransaction)
        .filter(
            FinancialTransaction.transaction_id == transaction_id
        )
        .count()
        == 1
    )
    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )

def test_commission_release_does_not_reuse_existing_completed_transaction_after_initial_miss(
    db,
    monkeypatch,
):
    owner = User(
        phone_number="09129991021",
        role="CUSTOMER",
        profile_completed=True,
    )
    referrer = User(
        phone_number="09129991022",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09129991023",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, referrer, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Commission Existing Transaction Race Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Commission Existing Transaction Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    end_time = datetime.now(timezone.utc) - timedelta(hours=4)
    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=end_time - timedelta(hours=1),
        end_time=end_time,
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=1,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status="COMPLETED",
    )
    db.add(booking)
    db.flush()

    reward_event = RewardEvent(
        user_id=referrer.id,
        business_id=business.id,
        booking_id=booking.id,
        idempotency_key="TEST-COMMISSION-RACE-001",
        type="REFERRAL_COMMISSION",
        amount=1000,
        status="PENDING",
    )
    treasury = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    wallet = Account(
        owner_type="USER",
        owner_id=referrer.id,
        account_type="CUSTOMER_WALLET",
        balance=250,
        currency="IRR",
        status="ACTIVE",
    )
    db.add_all([reward_event, treasury, wallet])
    db.flush()

    reward_event_id = reward_event.id
    treasury_id = treasury.id
    wallet_id = wallet.id
    transaction_id = f"COMMISSION-RELEASE-{reward_event_id}"

    existing_transaction = FinancialTransaction(
        transaction_id=transaction_id,
        type="COMMISSION_RELEASE",
        status="COMPLETED",
        total_amount=1000,
        reference_type="REWARD_EVENT",
        reference_id=reward_event_id,
    )
    db.add(existing_transaction)
    db.flush()

    # Simulate the balanced ledger already written by the first request.
    db.add_all([
        LedgerEntry(
            account_id=treasury_id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="DEBIT",
            amount=1000,
            reference_type="REWARD_EVENT",
            reference_id=reward_event_id,
        ),
        LedgerEntry(
            account_id=wallet_id,
            transaction_id=transaction_id,
            entry_type="COMMISSION_RELEASE",
            direction="CREDIT",
            amount=1000,
            reference_type="REWARD_EVENT",
            reference_id=reward_event_id,
        ),
    ])
    db.commit()

    # Simulate the initial lookup missing the transaction.
    monkeypatch.setattr(
        commission_release_service,
        "get_financial_transaction",
        lambda *args, **kwargs: None,
    )


    result = commission_release_service.release_commission(
        db,
        reward_event_id,
    )

    db.expire_all()

    reward_after = (
        db.query(RewardEvent)
        .filter(RewardEvent.id == reward_event_id)
        .one()
    )
    transaction_after = (
        db.query(FinancialTransaction)
        .filter(
            FinancialTransaction.transaction_id == transaction_id
        )
        .one()
    )

    actual = {
        "result_is_none": result is None,
        "treasury_balance": (
            db.query(Account).filter(Account.id == treasury_id).one().balance
        ),
        "wallet_balance": (
            db.query(Account).filter(Account.id == wallet_id).one().balance
        ),
        "transaction_count": (
            db.query(FinancialTransaction)
            .filter(
                FinancialTransaction.transaction_id == transaction_id
            )
            .count()
        ),
        "transaction_status": transaction_after.status,
        "ledger_entry_count": (
            db.query(LedgerEntry)
            .filter(LedgerEntry.transaction_id == transaction_id)
            .count()
        ),
        "reward_status": reward_after.status,
        "reward_transaction_id": reward_after.transaction_id,
    }

    expected = {
        "result_is_none": True,
        "treasury_balance": 5000,
        "wallet_balance": 250,
        "transaction_count": 1,
        "transaction_status": "COMPLETED",
        "ledger_entry_count": 2,
        "reward_status": "PENDING",
        "reward_transaction_id": None,
    }

    assert actual == expected


def test_commission_release_does_not_reuse_existing_pending_transaction_after_initial_miss(
    db,
    monkeypatch,
):
    owner = User(
        phone_number="09129991021",
        role="CUSTOMER",
        profile_completed=True,
    )
    referrer = User(
        phone_number="09129991022",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09129991023",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, referrer, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Commission Existing Transaction Race Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Commission Existing Transaction Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    end_time = datetime.now(timezone.utc) - timedelta(hours=4)
    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=end_time - timedelta(hours=1),
        end_time=end_time,
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=1,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status="COMPLETED",
    )
    db.add(booking)
    db.flush()

    reward_event = RewardEvent(
        user_id=referrer.id,
        business_id=business.id,
        booking_id=booking.id,
        idempotency_key="TEST-COMMISSION-RACE-002",
        type="REFERRAL_COMMISSION",
        amount=1000,
        status="PENDING",
    )
    treasury = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    wallet = Account(
        owner_type="USER",
        owner_id=referrer.id,
        account_type="CUSTOMER_WALLET",
        balance=250,
        currency="IRR",
        status="ACTIVE",
    )
    db.add_all([reward_event, treasury, wallet])
    db.flush()

    reward_event_id = reward_event.id
    treasury_id = treasury.id
    wallet_id = wallet.id
    transaction_id = f"COMMISSION-RELEASE-{reward_event_id}"

    existing_transaction = FinancialTransaction(
        transaction_id=transaction_id,
        type="COMMISSION_RELEASE",
        status="PENDING",
        total_amount=1000,
        reference_type="REWARD_EVENT",
        reference_id=reward_event_id,
    )
    db.add(existing_transaction)
    db.flush()

    # The existing pending transaction has no ledger entries yet.
    db.commit()

    # Simulate the initial lookup missing the transaction.
    monkeypatch.setattr(
        commission_release_service,
        "get_financial_transaction",
        lambda *args, **kwargs: None,
    )


    result = commission_release_service.release_commission(
        db,
        reward_event_id,
    )

    db.expire_all()

    reward_after = (
        db.query(RewardEvent)
        .filter(RewardEvent.id == reward_event_id)
        .one()
    )
    transaction_after = (
        db.query(FinancialTransaction)
        .filter(
            FinancialTransaction.transaction_id == transaction_id
        )
        .one()
    )

    actual = {
        "result_is_none": result is None,
        "treasury_balance": (
            db.query(Account).filter(Account.id == treasury_id).one().balance
        ),
        "wallet_balance": (
            db.query(Account).filter(Account.id == wallet_id).one().balance
        ),
        "transaction_count": (
            db.query(FinancialTransaction)
            .filter(
                FinancialTransaction.transaction_id == transaction_id
            )
            .count()
        ),
        "transaction_status": transaction_after.status,
        "ledger_entry_count": (
            db.query(LedgerEntry)
            .filter(LedgerEntry.transaction_id == transaction_id)
            .count()
        ),
        "reward_status": reward_after.status,
        "reward_transaction_id": reward_after.transaction_id,
    }

    expected = {
        "result_is_none": True,
        "treasury_balance": 5000,
        "wallet_balance": 250,
        "transaction_count": 1,
        "transaction_status": "PENDING",
        "ledger_entry_count": 0,
        "reward_status": "PENDING",
        "reward_transaction_id": None,
    }

    assert actual == expected
