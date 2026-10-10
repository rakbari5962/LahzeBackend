from difflib import SequenceMatcher

from sqlalchemy.orm import Session

from app.models.business_category import BusinessCategory
from app.repositories.category_alias_repository import get_alias_matches
from app.services import ai_category_service, category_llm_service
from app.services.category_normalization import normalize_category_text


MATCH_CATEGORY = "CATEGORY"
MATCH_ALIAS = "ALIAS"
MATCH_KEYWORD = "KEYWORD"
MATCH_PROPOSAL = "PROPOSAL"
MATCH_NONE = "NONE"

NEAR_DUPLICATE_RATIO = 0.85


def find_existing_category(
    db: Session,
    normalized_title: str,
    active_only: bool = True,
):
    """Deterministic identity lookup: canonical name, then managed alias.

    Returns (category, match_type) or (None, None). Compares normalized names in
    Python so rows whose `normalized_name` has not been backfilled still match.
    """
    query = db.query(BusinessCategory)
    if active_only:
        query = query.filter(BusinessCategory.is_active.is_(True))

    for category in query.all():
        if category.normalized_name == normalized_title or normalize_category_text(category.name) == normalized_title:
            return category, MATCH_CATEGORY

    for _alias, category in get_alias_matches(db, normalized_title):
        if category.is_active or not active_only:
            return category, MATCH_ALIAS

    return None, None


def find_near_duplicates(db: Session, normalized_title: str) -> list[dict]:
    """Possible (not certain) equivalents, for warnings and admin review."""
    matches = []
    for category in db.query(BusinessCategory).filter(BusinessCategory.is_active.is_(True)).all():
        candidate = normalize_category_text(category.name)
        if not candidate:
            continue
        ratio = SequenceMatcher(None, normalized_title, candidate).ratio()
        contains = len(candidate) >= 4 and (candidate in normalized_title or normalized_title in candidate)
        if ratio >= NEAR_DUPLICATE_RATIO or contains:
            matches.append({"id": category.id, "name": category.name})
    return matches


def _empty(match_type: str, reason: str) -> dict:
    return {
        "category_id": None,
        "category_name": None,
        "confidence": 0,
        "reason": reason,
        "match_type": match_type,
        "proposed_title": None,
        "warning": None,
        "possible_matches": [],
    }


def _existing(category, match_type: str, confidence: int, reason: str) -> dict:
    result = _empty(match_type, reason)
    result.update(category_id=category.id, category_name=category.name, confidence=confidence)
    return result


def resolve_category(
    db: Session,
    business_name: str,
    services: list[str] | None = None,
    description: str | None = None,
    allow_llm: bool = True,
) -> dict:
    """Resolve a business to an existing category, or propose a new title.

    Read-only. Order: canonical name, managed alias, keyword rules, then the LLM
    (only if everything deterministic failed). The LLM result is re-checked
    against existing categories and aliases before it is called a new proposal.
    """
    normalized_name = normalize_category_text(business_name)

    category, match_type = find_existing_category(db, normalized_name)
    if category is not None:
        label = "نام دسته‌بندی" if match_type == MATCH_CATEGORY else "نام مستعار ثبت‌شده"
        return _existing(
            category,
            match_type,
            100 if match_type == MATCH_CATEGORY else 95,
            f"بر اساس {label}، دسته‌بندی «{category.name}» پیشنهاد شد.",
        )

    keyword = ai_category_service.suggest_category(
        db=db,
        business_name=business_name,
        services=services,
        description=description,
    )
    if keyword.get("category_id") is not None:
        result = _empty(MATCH_KEYWORD, keyword["reason"])
        result.update(
            category_id=keyword["category_id"],
            category_name=keyword["category_name"],
            confidence=keyword["confidence"],
        )
        return result

    if not allow_llm:
        return _empty(MATCH_NONE, keyword["reason"])

    active = db.query(BusinessCategory).filter(BusinessCategory.is_active.is_(True)).all()
    try:
        title = category_llm_service.propose_category_title(
            business_name=business_name,
            services=services,
            description=description,
            existing_category_names=[c.name for c in active],
        )
    except Exception:
        # A misbehaving provider must never surface as an error to the client.
        return _empty(MATCH_NONE, "پیشنهاد خودکار در دسترس نیست؛ لطفاً دسته‌بندی را دستی انتخاب کنید.")
    if title is None:
        return _empty(MATCH_NONE, "پیشنهاد خودکار در دسترس نیست؛ لطفاً دسته‌بندی را دستی انتخاب کنید.")

    normalized_title = normalize_category_text(title)
    category, match_type = find_existing_category(db, normalized_title)
    if category is not None:
        return _existing(
            category,
            match_type,
            90,
            f"پیشنهاد هوشمند با دسته‌بندی موجود «{category.name}» یکسان بود.",
        )

    possible = find_near_duplicates(db, normalized_title)
    result = _empty(MATCH_PROPOSAL, "هیچ دسته‌بندی موجودی مناسب نبود؛ عنوان جدیدی پیشنهاد شد.")
    result["proposed_title"] = title
    result["possible_matches"] = possible
    if possible:
        result["warning"] = "این عنوان ممکن است با یک دسته‌بندی موجود معادل باشد؛ بررسی نهایی با مدیر است."
    return result
