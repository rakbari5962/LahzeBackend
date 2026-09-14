from sqlalchemy.orm import Session

from app.models.province import Province
from app.models.city import City


def get_provinces(
    db: Session
):
    return (
        db.query(Province)
        .order_by(Province.name)
        .all()
    )


def get_cities_by_province(
    db: Session,
    province_id: int
):
    return (
        db.query(City)
        .filter(
            City.province_id == province_id
        )
        .order_by(City.name)
        .all()
    )