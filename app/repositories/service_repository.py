from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate


def create_service(
    db: Session,
    service: ServiceCreate
):
    db_service = Service(
        business_id=service.business_id,
        name=service.name,
        base_price=service.base_price,
        duration_minutes=service.duration_minutes
    )

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service


def get_service(
    db: Session,
    service_id: int
):
    return db.query(Service).filter(
        Service.id == service_id
    ).first()