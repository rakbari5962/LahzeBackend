"""Registration (quarantine), dedup and transaction-integrity tests."""

import pytest

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401

from app.database.database import Base
from app.database.dependencies import get_db as app_get_db
from app.main import app
from app.models.business import Business
from app.models.category_alias import BusinessCategoryAlias
from app.models.category_proposal import (
    CategoryProposal,
    CategoryProposalBusiness,
    PROPOSAL_PENDING,
)
from app.services.business_service import create_business
from app.services import category_llm_service
from app.schemas.business import BusinessCreate


@pytest.fixture()
def client(db, monkeypatch):
    """TestClient wired to the isolated database; no real DB is reachable."""
    def override_get_db():
        yield db

    app.dependency_overrides[app_get_db] = override_get_db
    # No `with` block: that would run the startup hook and start the background
    # scheduler, which talks to the real database.
    yield TestClient(app)
    app.dependency_overrides.clear()


def _payload(**overrides):
    data = {
        "name": "کلینیک روانشناسی مهر",
        "province_id": 1,
        "city_id": 1,
        "services": ["مشاوره"],
        "description": None,
        "phone": None,
    }
    data.update(overrides)
    return data


def _no_llm(monkeypatch, title=None):
    monkeypatch.setattr(category_llm_service, "propose_category_title", lambda **kwargs: title)


# ------------------------------------------------------------------ suggestion

def test_suggestion_uses_alias_and_calls_no_llm(client, categories, monkeypatch):
    calls = []
    monkeypatch.setattr(
        category_llm_service,
        "propose_category_title",
        lambda **kwargs: calls.append(kwargs),
    )

    response = client.post("/businesses/suggest-category", json={"name": "Psychologist"})

    assert response.status_code == 200
    body = response.json()
    assert body["category_id"] == categories["health"].id
    assert body["match_type"] in ("ALIAS", "CATEGORY")
    assert calls == []


def test_suggestion_never_persists_a_proposal(client, db, categories, monkeypatch):
    _no_llm(monkeypatch, title="خدمات حقوقی")

    response = client.post("/businesses/suggest-category", json={"name": "مشاوره حقوقی و قراردادها"})

    assert response.status_code == 200
    assert response.json()["match_type"] == "PROPOSAL"
    assert response.json()["proposed_title"] == "خدمات حقوقی"
    assert db.query(CategoryProposal).count() == 0, "displaying a suggestion must not persist anything"


def test_suggestion_survives_a_failing_llm(client, categories, monkeypatch):
    def boom(**kwargs):
        raise RuntimeError("provider down")

    monkeypatch.setattr(category_llm_service, "propose_category_title", boom)

    response = client.post("/businesses/suggest-category", json={"name": "مشاوره حقوقی و قراردادها"})

    assert response.status_code == 200
    assert response.json()["match_type"] == "NONE"


# ------------------------------------------------------------- registration

def test_registration_with_existing_category_creates_no_proposal(db, owner, categories):
    created = create_business(
        db,
        BusinessCreate(**_payload(category_id=categories["beauty"].id)),
        owner.id,
    )

    assert created.category_id == categories["beauty"].id
    assert db.query(CategoryProposal).count() == 0
    assert db.query(CategoryProposalBusiness).count() == 0


def test_registration_with_proposal_quarantines_and_leaves_category_null(db, owner, categories):
    created = create_business(
        db,
        BusinessCreate(**_payload(proposed_category_title="خدمات حقوقی")),
        owner.id,
    )

    proposal = db.query(CategoryProposal).one()
    assert proposal.status == PROPOSAL_PENDING
    assert proposal.title == "خدمات حقوقی"
    assert created.category_id is None, "a pending business must not get a placeholder category"
    assert created.category_pending is True

    link = db.query(CategoryProposalBusiness).one()
    assert link.business_id == created.id
    assert link.proposal_id == proposal.id


def test_two_businesses_share_one_pending_proposal(db, owner, categories):
    first = create_business(db, BusinessCreate(**_payload(proposed_category_title="خدمات حقوقی")), owner.id)
    second = create_business(db, BusinessCreate(**_payload(name="دفتر حقوقی دوم", proposed_category_title="  خدمات حقوقی  ")), owner.id)

    assert db.query(CategoryProposal).count() == 1, "equivalent pending titles must deduplicate"
    assert db.query(CategoryProposalBusiness).count() == 2
    assert first.category_id is None and second.category_id is None


def test_proposal_equivalent_to_existing_category_reuses_it(db, owner, categories):
    created = create_business(
        db,
        BusinessCreate(**_payload(proposed_category_title="PSYCHOLOGIST")),
        owner.id,
    )

    assert created.category_id == categories["health"].id
    assert db.query(CategoryProposal).count() == 0, "an alias match must not create a proposal"


def test_category_id_and_proposed_title_are_mutually_exclusive(db, owner, categories):
    with pytest.raises(HTTPException) as exc:
        create_business(
            db,
            BusinessCreate(**_payload(category_id=categories["health"].id, proposed_category_title="خدمات حقوقی")),
            owner.id,
        )

    assert exc.value.status_code == 422
    assert db.query(Business).filter(Business.name == "کلینیک روانشناسی مهر").count() == 0


def test_invalid_category_id_is_rejected(db, owner, categories):
    with pytest.raises(HTTPException) as exc:
        create_business(db, BusinessCreate(**_payload(category_id=999999)), owner.id)

    assert exc.value.status_code == 422


def test_inactive_category_id_is_rejected(db, owner, categories):
    with pytest.raises(HTTPException) as exc:
        create_business(
            db,
            BusinessCreate(**_payload(category_id=categories["inactive"].id)),
            owner.id,
        )

    assert exc.value.status_code == 422


def test_invalid_proposed_title_is_rejected(db, owner, categories):
    with pytest.raises(HTTPException) as exc:
        create_business(db, BusinessCreate(**_payload(proposed_category_title="!")), owner.id)

    assert exc.value.status_code == 422
    assert db.query(Business).count() == 0


def test_registration_rolls_back_completely_when_a_later_step_fails(db, owner, categories, monkeypatch):
    """If the proposal step raises, the business must not survive."""
    from app.services import business_service

    def boom(**kwargs):
        raise RuntimeError("proposal step failed")

    monkeypatch.setattr(business_service, "attach_business_to_proposal", boom)

    with pytest.raises(RuntimeError):
        create_business(db, BusinessCreate(**_payload(proposed_category_title="خدمات حقوقی")), owner.id)

    assert db.query(Business).count() == 0, "the whole registration must roll back"
    assert db.query(CategoryProposal).count() == 0


def test_legacy_suggestion_still_runs_when_no_category_or_proposal(db, owner, categories, monkeypatch):
    """No category and no proposal: the pre-existing auto-suggestion stays."""
    created = create_business(db, BusinessCreate(**_payload(name="سالن زیبایی آترین")), owner.id)

    assert created.category_id is None
    assert created.category_pending is False