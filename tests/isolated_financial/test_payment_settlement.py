import app.models

from app.models.account import Account
from app.models.financial_transaction import FinancialTransaction
from app.models.ledger import LedgerEntry
from app.services.payment_service import create_payment
import app.services.settlement_service as settlement_service


def test_payment_is_recorded_once_with_balanced_ledger(db):
    wallet = Account(
        owner_type="USER",
        owner_id=1001,
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
    db.add_all([wallet, escrow])
    db.flush()

    first = create_payment(
        db,
        user_id=1001,
        amount=1200,
        booking_id=7001,
    )

    assert first is not None
    assert first["transaction"].status == "COMPLETED"
    assert first["transaction"].total_amount == 1200

    db.refresh(wallet)
    db.refresh(escrow)
    assert wallet.balance == 3800
    assert escrow.balance == 1200

    transaction_id = first["transaction"].transaction_id
    entries = (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .all()
    )

    assert len(entries) == 2
    assert sum(e.amount for e in entries) == 2400
    assert sum(e.amount for e in entries if e.direction == "DEBIT") == 1200
    assert sum(e.amount for e in entries if e.direction == "CREDIT") == 1200

    second = create_payment(
        db,
        user_id=1001,
        amount=1200,
        booking_id=7001,
    )

    assert second is not None
    assert second["transaction"].transaction_id == transaction_id

    db.refresh(wallet)
    db.refresh(escrow)
    assert wallet.balance == 3800
    assert escrow.balance == 1200

    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )


def test_payment_with_insufficient_balance_changes_nothing(db):
    wallet = Account(
        owner_type="USER",
        owner_id=1002,
        account_type="CUSTOMER_WALLET",
        balance=500,
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
    db.add_all([wallet, escrow])
    db.flush()
    db.commit()

    result = create_payment(
        db,
        user_id=1002,
        amount=1000,
        booking_id=7002,
    )

    assert result is None

    assert db.query(FinancialTransaction).count() == 0
    assert db.query(LedgerEntry).count() == 0

    assert (
        db.query(Account)
        .filter(
            Account.owner_type == "USER",
            Account.owner_id == 1002,
            Account.account_type == "CUSTOMER_WALLET",
        )
        .one()
        .balance
        == 500
    )

    assert (
        db.query(Account)
        .filter(
            Account.owner_type == "PLATFORM",
            Account.account_type == "ESCROW",
        )
        .one()
        .balance
        == 0
    )


def test_settlement_retry_does_not_transfer_money_twice(db, monkeypatch):
    monkeypatch.setattr(
        settlement_service,
        "trigger_settlement_rewards",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        settlement_service,
        "trigger_priority_access_rewards",
        lambda **kwargs: None,
    )

    escrow = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="ESCROW",
        balance=10000,
        currency="IRR",
        status="ACTIVE",
    )
    business = Account(
        owner_type="BUSINESS",
        owner_id=2001,
        account_type="BUSINESS_REVENUE",
        balance=0,
        currency="IRR",
        status="ACTIVE",
    )
    treasury = Account(
        owner_type="PLATFORM",
        owner_id=1,
        account_type="PLATFORM_TREASURY",
        balance=0,
        currency="IRR",
        status="ACTIVE",
    )
    db.add_all([escrow, business, treasury])
    db.flush()

    first = settlement_service.settle_payment(
        db,
        booking_id=8001,
        business_id=2001,
        amount=10000,
    )

    assert first is not None
    assert first["duplicate"] is False
    assert first["business_amount"] == 9500
    assert first["platform_amount"] == 500
    assert first["transaction"].status == "COMPLETED"

    db.refresh(escrow)
    db.refresh(business)
    db.refresh(treasury)

    assert escrow.balance == 0
    assert business.balance == 9500
    assert treasury.balance == 500

    transaction_id = first["transaction"].transaction_id

    second = settlement_service.settle_payment(
        db,
        booking_id=8001,
        business_id=2001,
        amount=10000,
    )

    assert second is not None
    assert second["duplicate"] is True
    assert second["transaction"].transaction_id == transaction_id

    db.refresh(escrow)
    db.refresh(business)
    db.refresh(treasury)

    assert escrow.balance == 0
    assert business.balance == 9500
    assert treasury.balance == 500

    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 3
    )


def test_payment_retry_rejects_debit_ledger_for_wrong_customer(db):
    wallet = Account(
        owner_type="USER", owner_id=1101,
        account_type="CUSTOMER_WALLET", balance=5000,
        currency="IRR", status="ACTIVE",
    )
    other_wallet = Account(
        owner_type="USER", owner_id=1102,
        account_type="CUSTOMER_WALLET", balance=7000,
        currency="IRR", status="ACTIVE",
    )
    escrow = Account(
        owner_type="PLATFORM", owner_id=1,
        account_type="ESCROW", balance=0,
        currency="IRR", status="ACTIVE",
    )
    db.add_all([wallet, other_wallet, escrow])
    db.flush()

    first = create_payment(
        db, user_id=1101, amount=1200, booking_id=7101,
    )
    assert first is not None

    transaction_id = first["transaction"].transaction_id
    debit = (
        db.query(LedgerEntry)
        .filter(
            LedgerEntry.transaction_id == transaction_id,
            LedgerEntry.direction == "DEBIT",
        )
        .one()
    )

    debit.account_id = other_wallet.id
    db.commit()

    db.refresh(wallet)
    db.refresh(other_wallet)
    db.refresh(escrow)
    before = (wallet.balance, other_wallet.balance, escrow.balance)

    retry = create_payment(
        db, user_id=1101, amount=1200, booking_id=7101,
    )

    assert retry is None

    db.refresh(wallet)
    db.refresh(other_wallet)
    db.refresh(escrow)
    assert (wallet.balance, other_wallet.balance, escrow.balance) == before
    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )


def test_payment_retry_rejects_credit_ledger_for_wrong_account(db):
    wallet = Account(
        owner_type="USER", owner_id=1103,
        account_type="CUSTOMER_WALLET", balance=5000,
        currency="IRR", status="ACTIVE",
    )
    escrow = Account(
        owner_type="PLATFORM", owner_id=1,
        account_type="ESCROW", balance=0,
        currency="IRR", status="ACTIVE",
    )
    treasury = Account(
        owner_type="PLATFORM", owner_id=1,
        account_type="PLATFORM_TREASURY", balance=0,
        currency="IRR", status="ACTIVE",
    )
    db.add_all([wallet, escrow, treasury])
    db.flush()

    first = create_payment(
        db, user_id=1103, amount=1200, booking_id=7102,
    )
    assert first is not None

    transaction_id = first["transaction"].transaction_id
    credit = (
        db.query(LedgerEntry)
        .filter(
            LedgerEntry.transaction_id == transaction_id,
            LedgerEntry.direction == "CREDIT",
        )
        .one()
    )

    credit.account_id = treasury.id
    db.commit()

    db.refresh(wallet)
    db.refresh(escrow)
    db.refresh(treasury)
    before = (wallet.balance, escrow.balance, treasury.balance)

    retry = create_payment(
        db, user_id=1103, amount=1200, booking_id=7102,
    )

    assert retry is None

    db.refresh(wallet)
    db.refresh(escrow)
    db.refresh(treasury)
    assert (wallet.balance, escrow.balance, treasury.balance) == before
    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )


def test_payment_retry_rejects_mismatched_ledger_amount(db):
    wallet = Account(
        owner_type="USER", owner_id=1104,
        account_type="CUSTOMER_WALLET", balance=5000,
        currency="IRR", status="ACTIVE",
    )
    escrow = Account(
        owner_type="PLATFORM", owner_id=1,
        account_type="ESCROW", balance=0,
        currency="IRR", status="ACTIVE",
    )
    db.add_all([wallet, escrow])
    db.flush()

    first = create_payment(
        db, user_id=1104, amount=1200, booking_id=7103,
    )
    assert first is not None

    transaction_id = first["transaction"].transaction_id
    debit = (
        db.query(LedgerEntry)
        .filter(
            LedgerEntry.transaction_id == transaction_id,
            LedgerEntry.direction == "DEBIT",
        )
        .one()
    )

    debit.amount = 1199
    db.commit()

    db.refresh(wallet)
    db.refresh(escrow)
    before = (wallet.balance, escrow.balance)

    retry = create_payment(
        db, user_id=1104, amount=1200, booking_id=7103,
    )

    assert retry is None

    db.refresh(wallet)
    db.refresh(escrow)
    assert (wallet.balance, escrow.balance) == before
    assert (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transaction_id == transaction_id)
        .count()
        == 2
    )
