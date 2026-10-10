from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.business import Business

from app.schemas.business import BusinessCreate


def create_business(
    db: Session,
    business: BusinessCreate,
    owner_user_id: int,
    commit: bool = True
):

    db_business = Business(
        name=business.name,
        owner_user_id=owner_user_id,
        category_id=business.category_id,
        province_id=business.province_id,
        city_id=business.city_id,
        description=business.description,
        phone=business.phone
    )

    db.add(db_business)

    if commit:
        db.commit()
        db.refresh(db_business)
    else:
        db.flush()

    return db_business


def get_businesses_by_owner(
    db: Session,
    owner_user_id: int
):

    return db.query(Business).filter(
        Business.owner_user_id == owner_user_id,
        Business.is_deleted == False,
    ).all()


def get_business(
    db: Session,
    business_id: int
):

    return db.query(Business).filter(
        Business.id == business_id,
        Business.is_deleted == False,
    ).first()


def get_business_for_update(
    db: Session,
    business_id: int,
):
    return (
        db.query(Business)
        .filter(Business.id == business_id)
        .with_for_update()
        .first()
    )


def update_business_location(
    db: Session,
    business_id: int,
    latitude: float,
    longitude: float,
    address: str | None = None
):

    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .with_for_update()
        .first()
    )

    if not business or business.is_deleted:
        return None

    business.latitude = latitude
    business.longitude = longitude
    business.address = address

    db.commit()
    db.refresh(business)

    return business


def update_business_profile(
    db: Session,
    business_id: int,
    description: str | None = None,
    phone: str | None = None
):

    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .with_for_update()
        .first()
    )

    if not business or business.is_deleted:
        return None

    business.description = description
    business.phone = phone

    db.commit()
    db.refresh(business)

    return business
