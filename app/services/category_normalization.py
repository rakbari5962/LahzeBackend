import re
import unicodedata


MAX_CATEGORY_TITLE_LENGTH = 60
MIN_CATEGORY_TITLE_LENGTH = 2

_ARABIC_TO_PERSIAN = str.maketrans(
    {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ۀ": "ه",
        "ة": "ه",
        "ؤ": "و",
        "أ": "ا",
        "إ": "ا",
        "ٱ": "ا",
    }
)

# Joiners / directional marks behave like a (half-)space between words.
_SPACE_LIKE = re.compile("[‌‍‎‏]")
# Characters with no visible width are deleted so words stay intact.
_DELETED = re.compile("[­ـ​﻿]")
_DIACRITICS = re.compile("[ً-ٰٟ]")
_PUNCTUATION = re.compile(r"[^\w\s]", flags=re.UNICODE)
_SPACES = re.compile(r"\s+")


def normalize_category_text(value: str | None) -> str:
    """Canonical identity form for names, aliases and proposals.

    The display title is never replaced by this value; it is only used for
    comparison, uniqueness and deduplication.
    """
    text = unicodedata.normalize("NFKC", value or "")
    text = text.translate(_ARABIC_TO_PERSIAN)
    text = _SPACE_LIKE.sub(" ", text)
    text = _DELETED.sub("", text)
    text = _DIACRITICS.sub("", text)
    text = _PUNCTUATION.sub(" ", text.replace("_", " "))
    text = _SPACES.sub(" ", text).strip()
    return text.casefold()


def clean_display_title(value: str | None) -> str:
    """Trim and collapse whitespace only; keeps the user's wording and casing."""
    return _SPACES.sub(" ", (value or "").strip())


def validate_category_title(value: str | None) -> tuple[str, str]:
    """Return (display_title, normalized_title) or raise ValueError."""
    title = clean_display_title(value)
    normalized = normalize_category_text(title)

    if len(normalized) < MIN_CATEGORY_TITLE_LENGTH:
        raise ValueError("عنوان دسته‌بندی بسیار کوتاه یا نامعتبر است.")

    if len(title) > MAX_CATEGORY_TITLE_LENGTH:
        raise ValueError("عنوان دسته‌بندی بیش از حد طولانی است.")

    if any(ord(char) < 32 for char in title):
        raise ValueError("عنوان دسته‌بندی شامل نویسه‌های نامعتبر است.")

    if not re.search(r"[^\W\d_]", normalized, flags=re.UNICODE):
        raise ValueError("عنوان دسته‌بندی باید شامل حروف باشد.")

    return title, normalized


def slugify_category(normalized_title: str) -> str:
    slug = re.sub(r"[^\w]+", "-", normalized_title, flags=re.UNICODE).strip("-_")
    return slug or "category"
