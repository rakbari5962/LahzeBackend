"""Category resolution: deterministic match -> alias -> keyword -> LLM fallback."""

from app.services import category_llm_service, category_resolution_service
from app.services.category_normalization import normalize_category_text, validate_category_title


def _no_llm(monkeypatch):
    calls = []

    def fake(**kwargs):
        calls.append(kwargs)
        return None

    monkeypatch.setattr(category_llm_service, "propose_category_title", fake)
    return calls


def test_exact_canonical_name_matches_without_llm(db, categories, monkeypatch):
    calls = _no_llm(monkeypatch)
    result = category_resolution_service.resolve_category(db, "سلامت و درمان")

    assert result["category_id"] == categories["health"].id
    assert result["match_type"] == "CATEGORY"
    assert calls == []


def test_psychologist_alias_matches_health_without_llm(db, categories, monkeypatch):
    calls = _no_llm(monkeypatch)
    result = category_resolution_service.resolve_category(db, "Psychologist")

    assert result["category_id"] == categories["health"].id
    assert result["category_name"] == "سلامت و درمان"
    assert result["match_type"] in ("ALIAS", "CATEGORY")
    assert calls == [], "the LLM must not be called when an alias matches"


def test_alias_matching_is_case_and_spacing_insensitive(db, categories, monkeypatch):
    _no_llm(monkeypatch)
    for name in ["  PSYCHOLOGIST ", "psychologist", "Psy­chologist"]:
        result = category_resolution_service.resolve_category(db, name)
        assert result["category_id"] == categories["health"].id, name


def test_inactive_category_is_never_selected(db, categories, monkeypatch):
    _no_llm(monkeypatch)
    result = category_resolution_service.resolve_category(db, "دسته غیرفعال")

    assert result["category_id"] != categories["inactive"].id
    assert result["match_type"] == "NONE"


def test_llm_is_called_only_after_deterministic_matching_fails(db, categories, monkeypatch):
    calls = []

    def fake(**kwargs):
        calls.append(kwargs)
        return "خدمات حقوقی"

    monkeypatch.setattr(category_llm_service, "propose_category_title", fake)
    result = category_resolution_service.resolve_category(db, "مشاوره حقوقی و قراردادها")

    assert len(calls) == 1
    assert result["match_type"] == "PROPOSAL"
    assert result["proposed_title"] == "خدمات حقوقی"
    assert result["category_id"] is None


def test_llm_output_duplicating_a_category_returns_that_category(db, categories, monkeypatch):
    monkeypatch.setattr(
        category_llm_service, "propose_category_title", lambda **kwargs: "سلامت و درمان"
    )
    result = category_resolution_service.resolve_category(db, "مشاوره حقوقی و قراردادها")

    assert result["category_id"] == categories["health"].id
    assert result["match_type"] == "CATEGORY"
    assert result["proposed_title"] is None


def test_llm_output_duplicating_an_alias_returns_that_category(db, categories, monkeypatch):
    monkeypatch.setattr(
        category_llm_service, "propose_category_title", lambda **kwargs: "PSYCHOLOGIST"
    )
    result = category_resolution_service.resolve_category(db, "مشاوره حقوقی و قراردادها")

    assert result["category_id"] == categories["health"].id
    assert result["proposed_title"] is None


def test_llm_failure_returns_a_safe_response(db, categories, monkeypatch):
    def boom(**kwargs):
        raise RuntimeError("provider exploded with secret details")

    monkeypatch.setattr(category_llm_service, "propose_category_title", boom)

    try:
        result = category_resolution_service.resolve_category(db, "مشاوره حقوقی و قراردادها")
    except RuntimeError:
        # Re-raising is also acceptable only if the route maps it; assert the
        # service itself stays safe instead.
        raise AssertionError("resolution must not leak provider errors")

    assert result["match_type"] == "NONE"
    assert result["proposed_title"] is None
    assert "secret" not in (result["reason"] or "")


def test_llm_can_be_disabled_entirely(db, categories, monkeypatch):
    calls = _no_llm(monkeypatch)
    result = category_resolution_service.resolve_category(
        db, "مشاوره حقوقی و قراردادها", allow_llm=False
    )

    assert result["match_type"] == "NONE"
    assert calls == []


def test_normalization_handles_arabic_variants_and_zwnj(db, categories, monkeypatch):
    _no_llm(monkeypatch)
    # Arabic yeh/kaf plus a ZWNJ instead of a normal space.
    result = category_resolution_service.resolve_category(db, "زیبايی و مراقبت شخصی")

    assert result["category_id"] == categories["beauty"].id


def test_short_token_does_not_create_false_positives(db, categories, monkeypatch):
    _no_llm(monkeypatch)
    # «مو» must not match inside unrelated words such as «موسسه».
    result = category_resolution_service.resolve_category(db, "موسسه ساختمانی")

    assert result["category_id"] != categories["beauty"].id


def test_validate_title_rejects_empty_and_overlong_titles():
    for bad in ["", "   ", "a", "x" * 61, "!!!" ]:
        try:
            validate_category_title(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should have been rejected")


def test_normalization_keeps_persian_letters_and_drops_punctuation():
    assert normalize_category_text("  سلامت، و درمان!  ") == normalize_category_text("سلامت و درمان")