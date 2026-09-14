from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.service import ServiceCreate, ServiceResponse
from app.repositories.service_repository import create_service, get_service


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.post(
    "/",
    response_model=ServiceResponse
)
def create_new_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    return create_service(db, service)


@router.get(
    "/{service_id}",
    response_model=ServiceResponse
)
def read_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    return get_service(db, service_id)