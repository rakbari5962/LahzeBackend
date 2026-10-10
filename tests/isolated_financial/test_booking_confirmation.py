from datetime import datetime, timedelta, timezone

import app.models

import pytest
from fastapi import HTTPException

import app.repositories.booking_repository as booking_repository

from app.models.user import User
from app.models.business import Business
from app.models.service import Service
from app.models.opportunity import Opportunity
from app.models.booking import Booking
from app.models.wallet_hold import WalletHold
from app.models.account import Account
from app.models.financial_transaction import FinancialTransaction
from app.models.ledger import LedgerEntry


def test_confirm_booking_success_and_retry_does_not_charge_twice(
    db,
    monkeypatch,
):
    # Isolate non-financial side effects.
    monkeypatch.setattr(
        booking_repository,
        "has_first_customer_access",
        lambda **kwargs: True,
    )
    monkeypatch.setattr(
        booking_repository,
        "create_notification",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        booking_repository,
        "send_booking_confirmation_notification",
        lambda **kwargs: None,
    )

    owner = User(
        phone_number="09121110011",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09121110012",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Isolated Payment Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Test Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    start_time = datetime.now(timezone.utc) + timedelta(days=1)

    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=start_time,
        end_time=start_time + timedelta(hours=1),
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=0,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status="PENDING_CONFIRMATION",
    )
    db.add(booking)
    db.flush()

    hold = WalletHold(
        user_id=customer.id,
        booking_id=booking.id,
        amount=1000,
        status="ACTIVE",
    )

    wallet = Account(
        owner_type="USER",
        owner_id=customer.id,
        account_type="CUSTOMER_WALLET",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    escrow = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="ESCROW",
        balance=0,
        currency="IRR",
        status="ACTIVE",
    )

    db.add_all([hold, wallet, escrow])
    db.commit()

    booking_id = booking.id
    hold_id = hold.id
    wallet_id = wallet.id
    escrow_id = escrow.id

    # First confirmation: payment must succeed.
    first = booking_repository.confirm_booking(
        db=db,
        booking_id=booking_id,
    )

    assert first is not None
    assert first.status == "CONFIRMED"

    persisted_hold = (
        db.query(WalletHold)
        .filter(WalletHold.id == hold_id)
        .one()
    )
    assert persisted_hold.status == "CAPTURED"

    db.expire_all()

    assert (
        db.query(Account).filter(Account.id == wallet_id).one().balance
        == 4000
    )
    assert (
        db.query(Account).filter(Account.id == escrow_id).one().balance
        == 1000
    )

    transaction_id = f"PAY-{booking_id}"

    transaction = (
        db.query(FinancialTransaction)
        .filter(FinancialTransaction.transaction_id == transaction_id)
        .one()
    )
    assert transaction.status == "COMPLETED"
    assert transaction.total_amount == 1000

    entries = (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .all()
    )
    assert len(entries) == 2
    assert sum(e.amount for e in entries if e.direction == "DEBIT") == 1000
    assert sum(e.amount for e in entries if e.direction == "CREDIT") == 1000

    # Second confirmation: must not charge the customer again.
    second = booking_repository.confirm_booking(
        db=db,
        booking_id=booking_id,
    )

    assert second is not None
    assert second.status == "CONFIRMED"

    db.expire_all()

    assert (
        db.query(Account).filter(Account.id == wallet_id).one().balance
        == 4000
    )
    assert (
        db.query(Account).filter(Account.id == escrow_id).one().balance
        == 1000
    )

    assert (
        db.query(FinancialTransaction)
        .filter(FinancialTransaction.transaction_id == transaction_id)
        .count()
        == 1
    )
    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )


def _create_confirmation_scenario(
    db,
    *,
    booking_status,
    hold_status,
):
    owner = User(
        phone_number="09121110101",
        role="CUSTOMER",
        profile_completed=True,
    )
    customer = User(
        phone_number="09121110102",
        role="CUSTOMER",
        profile_completed=True,
    )
    db.add_all([owner, customer])
    db.flush()

    business = Business(
        owner_user_id=owner.id,
        name="Isolated Rollback Test",
        status="ACTIVE",
        is_deleted=False,
    )
    db.add(business)
    db.flush()

    service = Service(
        business_id=business.id,
        name="Rollback Test Service",
        base_price=1000,
        duration_minutes=60,
        active=True,
    )
    db.add(service)
    db.flush()

    start_time = datetime.now(timezone.utc) + timedelta(days=1)

    opportunity = Opportunity(
        business_id=business.id,
        service_id=service.id,
        start_time=start_time,
        end_time=start_time + timedelta(hours=1),
        original_price=1000,
        discount_percent=0,
        final_price=1000,
        capacity=1,
        reserved_count=0,
        status="ACTIVE",
    )
    db.add(opportunity)
    db.flush()

    booking = Booking(
        user_id=customer.id,
        business_id=business.id,
        opportunity_id=opportunity.id,
        status=booking_status,
    )
    db.add(booking)
    db.flush()

    hold = WalletHold(
        user_id=customer.id,
        booking_id=booking.id,
        amount=1000,
        status=hold_status,
    )
    wallet = Account(
        owner_type="USER",
        owner_id=customer.id,
        account_type="CUSTOMER_WALLET",
        balance=5000,
        currency="IRR",
        status="ACTIVE",
    )
    escrow = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="ESCROW",
        balance=0,
        currency="IRR",
        status="ACTIVE",
    )

    db.add_all([hold, wallet, escrow])
    db.commit()

    return {
        "booking_id": booking.id,
        "hold_id": hold.id,
        "wallet_id": wallet.id,
        "escrow_id": escrow.id,
    }


def test_confirm_booking_payment_failure_rolls_back_hold_and_booking(
    db,
    monkeypatch,
):
    ids = _create_confirmation_scenario(
        db,
        booking_status="PENDING_CONFIRMATION",
        hold_status="ACTIVE",
    )

    # Force payment failure after the hold capture attempt.
    monkeypatch.setattr(
        booking_repository,
        "create_payment",
        lambda **kwargs: None,
    )

    result = booking_repository.confirm_booking(
        db=db,
        booking_id=ids["booking_id"],
    )

    assert result is None

    db.expire_all()

    persisted_booking = (
        db.query(Booking)
        .filter(Booking.id == ids["booking_id"])
        .one()
    )
    persisted_hold = (
        db.query(WalletHold)
        .filter(WalletHold.id == ids["hold_id"])
        .one()
    )

    assert persisted_booking.status == "PENDING_CONFIRMATION"
    assert persisted_hold.status == "ACTIVE"

    assert (
        db.query(Account)
        .filter(Account.id == ids["wallet_id"])
        .one()
        .balance
        == 5000
    )
    assert (
        db.query(Account)
        .filter(Account.id == ids["escrow_id"])
        .one()
        .balance
        == 0
    )

    assert db.query(FinancialTransaction).count() == 0
    assert db.query(LedgerEntry).count() == 0


def test_confirmed_booking_without_payment_is_rejected(
    db,
):
    ids = _create_confirmation_scenario(
        db,
        booking_status="CONFIRMED",
        hold_status="CAPTURED",
    )

    # A captured hold alone must not be treated as a completed payment.
    with pytest.raises(HTTPException) as exc_info:
        booking_repository.confirm_booking(
            db=db,
            booking_id=ids["booking_id"],
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "BOOKING_PAYMENT_INCONSISTENT"

    db.expire_all()

    persisted_booking = (
        db.query(Booking)
        .filter(Booking.id == ids["booking_id"])
        .one()
    )
    assert persisted_booking.status == "CONFIRMED"

    assert db.query(FinancialTransaction).count() == 0
    assert db.query(LedgerEntry).count() == 0
