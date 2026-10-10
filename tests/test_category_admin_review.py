"""Admin review lifecycle: authorization, state machine, atomicity, visibility."""

import pytest

from fastapi import HTTPException
from fastapi.testclient import TestClient

import app.models  # noqa: F401

from app.database.dependencies import get_db as app_get_db
from app.main import app
from app.models.business import Business
from app.models.business_category import BusinessCategory
from app.models.category_proposal import (
    CategoryProposal,
    CategoryProposalHistory,
    PROPOSAL_APPROVED,
    PROPOSAL_PENDING,
    PROPOSAL_REJECTED_REPLACED,
)
from app.schemas.business import BusinessCreate
from app.services import category_proposal_service as service
from app.services.business_service import create_business
from app.services.business_visibility_service import get_business_visibility_detail
from app.services.public_business_service import get_public_business_profile


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[app_get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _register(db, owner, title, name="دفتر حقوقی"):
    return create_business(
        db,
        BusinessCreate(
            name=name,
            province_id=1,
            city_id=1,
            services=["مشاوره"],
            proposed_category_title=title,
        ),
        owner.id,
    )


def _admin_headers():
    return {"X-Session-Token": "admin-session-token"}


# ------------------------------------------------------------ authorization

def test_unauthenticated_cannot_list_or_review(client, db, owner, categories):
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id

    assert client.get("/admin/category-proposals/").status_code in (401, 422)
    assert client.get(f"/admin/category-proposals/{proposal_id}").status_code in (401, 422)
    assert client.post(f"/admin/category-proposals/{proposal_id}/approve").status_code in (401, 422)
    assert (
        client.post(
            f"/admin/category-proposals/{proposal_id}/reject",
            json={"replacement_title": "حقوقی"},
        ).status_code
        in (401, 422)
    )
    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING


def test_non_admin_cannot_review(client, db, owner, categories, customer_session):
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    headers = {"X-Session-Token": "customer-session-token"}

    assert client.get("/admin/category-proposals/", headers=headers).status_code == 403
    assert client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=headers).status_code == 403
    assert (
        client.post(
            f"/admin/category-proposals/{proposal_id}/reject",
            json={"replacement_title": "حقوقی"},
            headers=headers,
        ).status_code
        == 403
    )
    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING


def test_legacy_suggestion_review_requires_admin(client, db, categories):
    assert client.patch("/category-suggestions/1/approve").status_code in (401, 422)
    assert client.patch("/category-suggestions/1/reject").status_code in (401, 422)


# ------------------------------------------------------------------- queue

def test_admin_lists_and_reads_pending_proposals(client, db, owner, categories, admin_session):
    _register(db, owner, "خدمات حقوقی")

    listing = client.get("/admin/category-proposals/", headers=_admin_headers())
    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    item = listing.json()["items"][0]
    assert item["title"] == "خدمات حقوقی"
    assert item["status"] == PROPOSAL_PENDING

    detail = client.get(f"/admin/category-proposals/{item['id']}", headers=_admin_headers())
    assert detail.status_code == 200
    assert len(detail.json()["businesses"]) == 1
    assert detail.json()["history"] == []


def test_missing_proposal_is_404(client, categories, admin_session):
    assert client.get("/admin/category-proposals/9999", headers=_admin_headers()).status_code == 404


# ---------------------------------------------------------------- approve

def test_approve_creates_category_assigns_businesses_and_writes_history(
    client, db, owner, categories, admin, admin_session
):
    first = _register(db, owner, "خدمات حقوقی", name="دفتر یک")
    second = _register(db, owner, "خدمات حقوقی", name="دفتر دو")
    proposal_id = db.query(CategoryProposal).one().id
    before = db.query(BusinessCategory).count()

    response = client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=_admin_headers())

    assert response.status_code == 200
    assert db.query(BusinessCategory).count() == before + 1

    proposal = db.query(CategoryProposal).one()
    category = db.query(BusinessCategory).filter(BusinessCategory.name == "خدمات حقوقی").one()
    assert proposal.status == PROPOSAL_APPROVED
    assert proposal.final_category_id == category.id
    assert proposal.reviewed_by_user_id == admin.id
    assert proposal.title == "خدمات حقوقی"

    db.refresh(first)
    db.refresh(second)
    assert first.category_id == category.id
    assert second.category_id == category.id

    history = db.query(CategoryProposalHistory).one()
    assert history.original_title == "خدمات حقوقی"
    assert history.decision == "APPROVED"
    assert history.final_category_id == category.id
    assert history.admin_user_id == admin.id


def test_approve_reuses_a_category_created_after_the_proposal(client, db, owner, categories, admin_session):
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    existing = BusinessCategory(name="خدمات حقوقی", slug="legal", is_active=True)
    db.add(existing)
    db.flush()
    before = db.query(BusinessCategory).count()

    response = client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=_admin_headers())

    assert response.status_code == 200
    assert db.query(BusinessCategory).count() == before, "must not create a duplicate category"
    assert db.query(CategoryProposal).one().final_category_id == existing.id


def test_new_category_gets_a_unique_slug(client, db, owner, categories, admin_session):
    db.add(BusinessCategory(name="چیز دیگر", slug="خدمات-حقوقی", is_active=True))
    db.flush()
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id

    response = client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=_admin_headers())

    assert response.status_code == 200
    slugs = [c.slug for c in db.query(BusinessCategory).filter(BusinessCategory.name == "خدمات حقوقی")]
    assert len(slugs) == 1 and slugs[0] != "خدمات-حقوقی"


def test_completed_proposal_cannot_be_reviewed_again(client, db, owner, categories, admin_session):
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    assert client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=_admin_headers()).status_code == 200
    count = db.query(BusinessCategory).count()

    again = client.post(f"/admin/category-proposals/{proposal_id}/approve", headers=_admin_headers())
    rejected = client.post(
        f"/admin/category-proposals/{proposal_id}/reject",
        json={"replacement_title": "چیز دیگر"},
        headers=_admin_headers(),
    )

    assert again.status_code == 409
    assert rejected.status_code == 409
    assert db.query(BusinessCategory).count() == count
    assert db.query(CategoryProposalHistory).count() == 1


# ----------------------------------------------------------------- reject

def test_reject_requires_a_replacement_title(client, db, owner, categories, admin_session):
    _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id

    for body in [{}, {"replacement_title": ""}, {"replacement_title": " "}, {"replacement_title": "x" * 61}]:
        response = client.post(
            f"/admin/category-proposals/{proposal_id}/reject", json=body, headers=_admin_headers()
        )
        assert response.status_code == 422, body

    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING


def test_reject_with_new_replacement_registers_the_replacement_not_the_original(
    client, db, owner, categories, admin, admin_session
):
    business = _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id

    response = client.post(
        f"/admin/category-proposals/{proposal_id}/reject",
        json={"replacement_title": "وکالت و مشاوره", "note": "عنوان دقیق‌تر"},
        headers=_admin_headers(),
    )

    assert response.status_code == 200
    assert db.query(BusinessCategory).filter(BusinessCategory.name == "خدمات حقوقی").count() == 0
    replacement = db.query(BusinessCategory).filter(BusinessCategory.name == "وکالت و مشاوره").one()

    proposal = db.query(CategoryProposal).one()
    assert proposal.status == PROPOSAL_REJECTED_REPLACED
    assert proposal.title == "خدمات حقوقی", "the original proposal title must be preserved"
    assert proposal.final_category_id == replacement.id

    db.refresh(business)
    assert business.category_id == replacement.id

    history = db.query(CategoryProposalHistory).one()
    assert history.original_title == "خدمات حقوقی"
    assert history.replacement_title == "وکالت و مشاوره"
    assert history.final_category_id == replacement.id
    assert history.note == "عنوان دقیق‌تر"
    assert history.decision == "REJECTED_WITH_REPLACEMENT"


def test_reject_with_equivalent_replacement_reuses_existing_category(
    client, db, owner, categories, admin_session
):
    business = _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    before = db.query(BusinessCategory).count()

    response = client.post(
        f"/admin/category-proposals/{proposal_id}/reject",
        json={"replacement_title": "  PSYCHOLOGIST "},
        headers=_admin_headers(),
    )

    assert response.status_code == 200
    assert db.query(BusinessCategory).count() == before
    db.refresh(business)
    assert business.category_id == categories["health"].id


# -------------------------------------------------------------- atomicity

def test_approve_rolls_back_everything_when_history_fails(db, owner, categories, admin, monkeypatch):
    business = _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    before = db.query(BusinessCategory).count()

    original_finish = service._finish

    def failing_finish(*args, **kwargs):
        original_finish(*args, **kwargs)
        raise RuntimeError("history write failed")

    monkeypatch.setattr(service, "_finish", failing_finish)

    with pytest.raises(RuntimeError):
        service.approve_proposal(db, proposal_id, admin.id)

    assert db.query(BusinessCategory).count() == before, "category creation must roll back"
    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING
    assert db.query(CategoryProposalHistory).count() == 0
    db.refresh(business)
    assert business.category_id is None


def test_reject_rolls_back_everything_on_failure(db, owner, categories, admin, monkeypatch):
    business = _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    before = db.query(BusinessCategory).count()

    def boom(*args, **kwargs):
        raise RuntimeError("assignment failed")

    monkeypatch.setattr(service, "_assign_category_to_linked_businesses", boom)

    with pytest.raises(RuntimeError):
        service.reject_proposal_with_replacement(db, proposal_id, admin.id, "وکالت و مشاوره")

    assert db.query(BusinessCategory).count() == before
    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING
    assert db.query(CategoryProposalHistory).count() == 0
    db.refresh(business)
    assert business.category_id is None


def test_approval_aborts_if_a_business_category_changed_meanwhile(db, owner, categories, admin):
    business = _register(db, owner, "خدمات حقوقی")
    proposal_id = db.query(CategoryProposal).one().id
    business.category_id = categories["beauty"].id  # changed by another operation
    db.commit()
    before = db.query(BusinessCategory).count()

    with pytest.raises(HTTPException) as exc:
        service.approve_proposal(db, proposal_id, admin.id)

    assert exc.value.status_code == 409
    assert db.query(BusinessCategory).count() == before
    assert db.query(CategoryProposal).one().status == PROPOSAL_PENDING
    db.refresh(business)
    assert business.category_id == categories["beauty"].id


# -------------------------------------------------------------- visibility

def test_pending_business_is_hidden_then_visible_after_approval(db, owner, categories, admin):
    business = _register(db, owner, "خدمات حقوقی")

    detail = get_business_visibility_detail(db=db, business_id=business.id)
    assert "CATEGORY_PENDING_REVIEW" in detail["reason"]
    assert detail["visible"] is False
    assert get_public_business_profile(db=db, business_id=business.id) is None

    service.approve_proposal(db, db.query(CategoryProposal).one().id, admin.id)

    detail = get_business_visibility_detail(db=db, business_id=business.id)
    assert "CATEGORY_PENDING_REVIEW" not in (detail["reason"] or [])


def test_categorized_business_is_unaffected(db, owner, categories):
    business = create_business(
        db,
        BusinessCreate(
            name="سالن زیبایی",
            province_id=1,
            city_id=1,
            services=["کوتاهی"],
            category_id=categories["beauty"].id,
        ),
        owner.id,
    )

    detail = get_business_visibility_detail(db=db, business_id=business.id)
    assert "CATEGORY_PENDING_REVIEW" not in (detail["reason"] or [])


def test_pending_business_stays_visible_to_its_owner_record(db, owner, categories):
    business = _register(db, owner, "خدمات حقوقی")

    assert db.query(Business).filter(Business.id == business.id, Business.owner_user_id == owner.id).count() == 1
    assert service.get_pending_proposal_for_business(db, business.id) is not None