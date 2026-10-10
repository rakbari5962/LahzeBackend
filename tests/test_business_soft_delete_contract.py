from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_deletion_service_is_soft_delete_and_fail_closed():
    src = read("app/services/business_deletion_service.py")
    assert "with_for_update()" in src
    assert "business.is_deleted = True" in src
    assert "db.delete(" not in src
    assert '"PENDING_CONFIRMATION"' in src
    assert '"CONFIRMED"' in src
    assert '"NO_SHOW_REPORTED"' in src
    assert '"ACTIVE_WALLET_HOLD"' in src
    assert '"NON_COMPLETED_FINANCIAL_TRANSACTION"' in src
    assert 'status == "EXPIRED"' in src
    assert 'end_time <= now' in src


def test_pending_reward_events_are_not_independent_blockers():
    src = read("app/services/business_deletion_service.py")
    assert "RewardEvent status is intentionally not used as an independent blocker." in src
    assert "event.status" not in src


def test_business_delete_route_uses_backend_session_and_service():
    src = read("app/api/routes/businesses.py")
    assert '@router.delete(' in src
    assert '"/{business_id}"' in src
    assert "get_login_session" in src
    assert "session.user_id" in src
    assert "delete_business(" in src


def test_deleted_business_is_hidden_and_blocks_opportunity_creation():
    business_repo = read("app/repositories/business_repository.py")
    opportunity_repo = read("app/repositories/opportunity_repository.py")
    assert "Business.is_deleted == False" in business_repo
    assert ".with_for_update()" in opportunity_repo
    assert 'business.is_deleted' in opportunity_repo
    assert 'detail="BUSINESS_DELETED"' in opportunity_repo


def test_booking_creation_locks_business_and_rejects_deleted_business():
    src = read("app/repositories/booking_repository.py")
    assert ".with_for_update()" in src
    assert 'business.is_deleted' in src
    assert 'detail="BUSINESS_DELETED"' in src
