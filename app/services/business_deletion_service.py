from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.booking import Booking
from app.models.financial_transaction import FinancialTransaction
from app.models.no_show_report import NoShowReport
from app.models.opportunity import Opportunity
from app.models.reward_event import RewardEvent
from app.models.wallet_hold import WalletHold


BLOCKING_BOOKING_STATUSES = {
    "PENDING_CONFIRMATION",
    "CONFIRMED",
    "NO_SHOW_REPORTED",
}
TERMINAL_BOOKING_STATUSES = {
    "CANCELLED",
    "COMPLETED",
}
KNOWN_NON_TERMINAL_NO_SHOW_STATUSES = {"PENDING"}
KNOWN_TERMINAL_NO_SHOW_STATUSES = {"CUSTOMER_DISPUTED"}
TERMINAL_WALLET_HOLD_STATUSES = {"RELEASED", "CAPTURED"}


def _blocked(blocker_type: str, count: int, **details: Any) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": blocker_type,
        "count": count,
    }
    item.update(details)
    return item


def _raise_blocked(blockers: list[dict[str, Any]]) -> None:
    raise HTTPException(
        status_code=409,
        detail={
            "error": "BUSINESS_DELETION_BLOCKED",
            "blockers": blockers,
        },
    )


def _lock_business(db: Session, business_id: int) -> Business | None:
    return (
        db.execute(
            select(Business)
            .where(Business.id == business_id)
            .with_for_update()
        )
        .scalars()
        .first()
    )


def delete_business(
    db: Session,
    business_id: int,
    owner_user_id: int,
):
    """Soft-delete a Business atomically after a fail-closed eligibility check."""
    business = _lock_business(db, business_id)

    if not business:
        raise HTTPException(status_code=404, detail="BUSINESS_NOT_FOUND")

    if business.owner_user_id != owner_user_id:
        raise HTTPException(status_code=403, detail="BUSINESS_OWNER_REQUIRED")

    if business.is_deleted:
        raise HTTPException(status_code=409, detail="BUSINESS_ALREADY_DELETED")

    now = datetime.now(timezone.utc)
    blockers: list[dict[str, Any]] = []

    bookings = db.execute(
        select(Booking).where(Booking.business_id == business_id)
    ).scalars().all()

    non_terminal_bookings = [
        booking
        for booking in bookings
        if booking.status not in TERMINAL_BOOKING_STATUSES
    ]
    known_non_terminal_bookings = [
        booking
        for booking in non_terminal_bookings
        if booking.status in BLOCKING_BOOKING_STATUSES
    ]
    unknown_bookings = [
        booking
        for booking in non_terminal_bookings
        if booking.status not in BLOCKING_BOOKING_STATUSES
    ]

    if known_non_terminal_bookings:
        blockers.append(
            _blocked(
                "NON_TERMINAL_BOOKING",
                len(known_non_terminal_bookings),
                statuses=sorted(
                    {booking.status for booking in known_non_terminal_bookings}
                ),
            )
        )

    if unknown_bookings:
        blockers.append(
            _blocked(
                "NON_TERMINAL_BOOKING_UNKNOWN_STATUS",
                len(unknown_bookings),
            )
        )

    no_show_reports = db.execute(
        select(NoShowReport).where(NoShowReport.business_id == business_id)
    ).scalars().all()

    pending_no_shows = [
        report for report in no_show_reports if report.status == "PENDING"
    ]
    unknown_no_shows = [
        report
        for report in no_show_reports
        if report.status not in KNOWN_NON_TERMINAL_NO_SHOW_STATUSES
        and report.status not in KNOWN_TERMINAL_NO_SHOW_STATUSES
    ]

    if pending_no_shows:
        blockers.append(
            _blocked("PENDING_NO_SHOW", len(pending_no_shows))
        )

    if unknown_no_shows:
        blockers.append(
            _blocked("UNKNOWN_NO_SHOW_STATUS", len(unknown_no_shows))
        )

    opportunities = db.execute(
        select(Opportunity).where(Opportunity.business_id == business_id)
    ).scalars().all()

    non_terminal_opportunities = [
        opportunity
        for opportunity in opportunities
        if not (
            opportunity.status == "EXPIRED"
            and opportunity.end_time is not None
            and opportunity.end_time <= now
        )
    ]

    if non_terminal_opportunities:
        blockers.append(
            _blocked(
                "NON_TERMINAL_OPPORTUNITY",
                len(non_terminal_opportunities),
                statuses=sorted(
                    {
                        opportunity.status
                        for opportunity in non_terminal_opportunities
                    }
                ),
            )
        )

    booking_ids = [booking.id for booking in bookings]

    if booking_ids:
        holds = db.execute(
            select(WalletHold).where(WalletHold.booking_id.in_(booking_ids))
        ).scalars().all()

        active_holds = [
            hold for hold in holds if hold.status == "ACTIVE"
        ]
        unknown_holds = [
            hold
            for hold in holds
            if hold.status not in ("ACTIVE", *TERMINAL_WALLET_HOLD_STATUSES)
        ]

        if active_holds:
            blockers.append(
                _blocked("ACTIVE_WALLET_HOLD", len(active_holds))
            )

        if unknown_holds:
            blockers.append(
                _blocked("UNKNOWN_WALLET_HOLD_STATUS", len(unknown_holds))
            )
    else:
        holds = []

    reward_events = db.execute(
        select(RewardEvent).where(RewardEvent.business_id == business_id)
    ).scalars().all()

    reference_ids: list[int] = list(booking_ids)
    reward_event_ids = [event.id for event in reward_events]

    financial_transactions = []
    if reference_ids or reward_event_ids:
        transaction_filters = []
        if reference_ids:
            transaction_filters.append(
                (FinancialTransaction.reference_type == "BOOKING")
                & FinancialTransaction.reference_id.in_(reference_ids)
            )
        if reward_event_ids:
            transaction_filters.append(
                (FinancialTransaction.reference_type == "REWARD_EVENT")
                & FinancialTransaction.reference_id.in_(reward_event_ids)
            )

        transaction_condition = transaction_filters[0]
        for extra_condition in transaction_filters[1:]:
            transaction_condition = transaction_condition | extra_condition

        financial_transactions = db.execute(
            select(FinancialTransaction).where(transaction_condition)
        ).scalars().all()

    non_completed_financial_transactions = [
        transaction
        for transaction in financial_transactions
        if transaction.status != "COMPLETED"
    ]

    if non_completed_financial_transactions:
        blockers.append(
            _blocked(
                "NON_COMPLETED_FINANCIAL_TRANSACTION",
                len(non_completed_financial_transactions),
                statuses=sorted(
                    {
                        transaction.status
                        for transaction in non_completed_financial_transactions
                    }
                ),
            )
        )

    # RewardEvent status is intentionally not used as an independent blocker.
    # FinancialTransactions linked to RewardEvents are checked above.

    if blockers:
        db.rollback()
        _raise_blocked(blockers)

    business.is_deleted = True
    db.commit()
    db.refresh(business)

    return business
