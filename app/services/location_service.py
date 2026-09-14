from sqlalchemy.orm import Session

from app.repositories.location_repository import (
    get_provinces,
    get_cities_by_province
)


def list_provinces(
    db: Session
):
    return get_provinces(
        db=db
    )


def list_cities_by_province(
    db: Session,
    province_id: int
):
    return get_cities_by_province(
        db=db,
        province_id=province_id
    )