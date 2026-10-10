from types import SimpleNamespace

from app.services import ai_category_service


def _category(category_id, name, slug, is_active=True):
    return SimpleNamespace(id=category_id, name=name, slug=slug, is_active=is_active)


def _set_categories(monkeypatch, categories):
    monkeypatch.setattr(ai_category_service, "get_categories", lambda _db: categories)


def test_suggest_category_maps_existing_active_category(monkeypatch):
    categories = [_category(1, "زیبایی و مراقبت شخصی", "beauty"), _category(2, "رستوران و کافه", "restaurant")]
    _set_categories(monkeypatch, categories)
    result = ai_category_service.suggest_category(None, "سالن زیبایی آترین", ["رنگ مو"])
    assert result["category_id"] == 1
    assert result["category_name"] == "زیبایی و مراقبت شخصی"
    assert 0 < result["confidence"] <= 100


def test_unmatched_name_has_no_suggestion(monkeypatch):
    _set_categories(monkeypatch, [_category(1, "زیبایی", "beauty")])
    result = ai_category_service.suggest_category(None, "شرکت نمونه افق", [])
    assert result["category_id"] is None
    assert result["confidence"] == 0


def test_inactive_or_missing_slug_is_never_returned(monkeypatch):
    _set_categories(monkeypatch, [_category(1, "دسته غیرفعال", "beauty", False)])
    result = ai_category_service.suggest_category(None, "سالن زیبایی آترین", [])
    assert result["category_id"] is None


def test_arabic_yeh_kaf_and_zwnj_are_normalized(monkeypatch):
    _set_categories(monkeypatch, [_category(1, "زیبایی", "beauty")])
    result = ai_category_service.suggest_category(None, "سالن زيبايی آترین", ["رنگ‌مو"])
    assert result["category_id"] == 1


def test_short_keyword_does_not_match_substring(monkeypatch):
    _set_categories(monkeypatch, [_category(1, "زیبایی", "beauty")])
    result = ai_category_service.suggest_category(None, "نمونه", [])
    assert result["category_id"] is None


def test_tied_scores_do_not_choose_arbitrarily(monkeypatch):
    categories = [_category(1, "زیبایی", "beauty"), _category(2, "خدمات خانه", "home-services")]
    _set_categories(monkeypatch, categories)
    result = ai_category_service.suggest_category(None, "خدمات خانه و زیبایی", [])
    assert result["category_id"] is None
    assert "مشابه" in result["reason"]


def test_confidence_is_heuristic_integer_bounded_0_100(monkeypatch):
    _set_categories(monkeypatch, [_category(1, "رستوران", "restaurant")])
    result = ai_category_service.suggest_category(None, "کافه قهوه کیک", [])
    assert isinstance(result["confidence"], int)
    assert 0 <= result["confidence"] <= 100
