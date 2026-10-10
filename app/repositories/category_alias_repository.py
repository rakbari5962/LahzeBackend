from sqlalchemy.orm import Session

from app.models.business_category import BusinessCategory
from app.models.category_alias import BusinessCategoryAlias
from app.services.category_normalization import normalize_category_text


def get_alias_matches(db: Session, normalized_alias: str):
    return (
        db.query(BusinessCategoryAlias, BusinessCategory)
        .join(BusinessCategory, BusinessCategory.id == BusinessCategoryAlias.category_id)
        .filter(
            BusinessCategoryAlias.normalized_alias == normalized_alias,
            BusinessCategory.is_active.is_(True),
        )
        .all()
    )


def create_alias(
    db: Session,
    category_id: int,
    alias: str,
):
    return BusinessCategoryAlias(
        category_id=category_id,
        alias=alias.strip(),
        normalized_alias=normalize_category_text(alias),
    )
