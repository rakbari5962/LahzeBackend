import re
import unicodedata

from sqlalchemy.orm import Session

from app.repositories.business_category_repository import get_categories


KEYWORDS_BY_SLUG: dict[str, tuple[str, ...]] = {
    "beauty": ("مو", "آرایش", "آرایشگر", "زیبایی", "ناخن", "مژه", "ابرو", "پوست", "کراتین", "رنگ مو", "رنگ"),
    "restaurant": ("رستوران", "کافه", "غذا", "قهوه", "فست فود", "کیک", "آشپزی"),
    "health": ("پزشک", "کلینیک", "درمان", "دندان", "سلامت", "درمانی", "پرستاری"),
    "home-services": ("تعمیر", "کولر", "لوله", "برق", "خانه", "لوله کشی", "تاسیسات"),
    "education": ("آموزش", "کلاس", "دوره", "زبان", "موسیقی", "آموزشگاه", "معلم"),
    "fitness": ("باشگاه", "ورزش", "بدنسازی", "یوگا", "تناسب اندام", "مربی ورزشی"),
    "automotive": ("خودرو", "ماشین", "موتور", "تعمیرگاه", "مکانیکی", "کارواش"),
    "retail": ("فروشگاه", "فروش", "محصول", "لباس", "پوشاک", "خرده فروشی"),
}


def _normalize_persian(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("ي", "ی").replace("ى", "ی").replace("ك", "ک")
    value = value.replace("ۀ", "ه").replace("ة", "ه")
    value = value.replace("‌", " ").replace("‏", " ").replace("‎", " ")
    value = re.sub(r"[ً-ٰٟ]", "", value)
    value = re.sub(r"[\sـ]+", " ", value).strip().lower()
    return value


def _keyword_matches(text: str, keyword: str) -> bool:
    normalized_keyword = _normalize_persian(keyword)
    if not normalized_keyword:
        return False
    # Short Persian terms such as «مو» must match as a complete token.
    if len(normalized_keyword.replace(" ", "")) <= 2:
        return re.search(
            rf"(?<![\w]){re.escape(normalized_keyword)}(?![\w])",
            text,
            flags=re.UNICODE,
        ) is not None
    # Multi-word phrases are matched after normalizing ZWNJ and spacing.
    if " " in normalized_keyword:
        return f" {normalized_keyword} " in f" {text} "
    # Longer terms permit Persian suffixes (e.g. آرایشگر) while still avoiding
    # matching tiny substrings.
    return normalized_keyword in text


def _no_suggestion(reason: str) -> dict[str, int | str | None]:
    return {"category_id": None, "category_name": None, "confidence": 0, "reason": reason}


def suggest_category(
    db: Session,
    business_name: str,
    services: list[str] | None = None,
    description: str | None = None,
) -> dict[str, int | str | None]:
    """Return a rule-based suggestion; confidence is a keyword-match score, not probability."""
    categories = [category for category in get_categories(db) if category.is_active]
    if not categories:
        return _no_suggestion("دسته‌بندی فعالی برای بررسی در سیستم موجود نیست.")

    text = _normalize_persian(" ".join([business_name, *(services or []), description or ""]))
    active_by_slug = {category.slug: category for category in categories}
    scores: dict[str, int] = {}
    for slug, keywords in KEYWORDS_BY_SLUG.items():
        if slug not in active_by_slug:
            continue
        scores[slug] = sum(1 for keyword in keywords if _keyword_matches(text, keyword))

    if not scores:
        return _no_suggestion("دسته‌بندی‌های فعال با قواعد فعلی پیشنهاد تطبیق ندارند؛ لطفاً دستی انتخاب کنید.")

    best_score = max(scores.values())
    if best_score <= 0:
        return _no_suggestion("برای پیشنهاد دسته‌بندی مناسب، اطلاعات بیشتری وارد کنید.")

    winners = sorted(slug for slug, score in scores.items() if score == best_score)
    if len(winners) != 1:
        return _no_suggestion("چند دسته‌بندی تطبیق مشابه دارند؛ لطفاً دسته‌بندی را دستی انتخاب کنید.")

    category = active_by_slug[winners[0]]
    # This deterministic heuristic score reports number of keyword hits, not a calibrated probability.
    confidence = min(best_score * 20, 95)
    return {
        "category_id": category.id,
        "category_name": category.name,
        "confidence": confidence,
        "reason": f"بر اساس تطبیق {best_score} کلیدواژه در نام، خدمات یا توضیحات، دسته‌بندی «{category.name}» پیشنهاد شد.",
    }
