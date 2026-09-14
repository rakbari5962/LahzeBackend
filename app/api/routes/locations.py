from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.province import ProvinceResponse
from app.schemas.city import CityResponse

from app.services.location_service import (
    list_provinces,
    list_cities_by_province
)


router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.get(
    "/provinces",
    response_model=list[ProvinceResponse]
)
def read_provinces(
    db: Session = Depends(get_db)
):
    return list_provinces(
        db=db
    )


@router.get(
    "/provinces/{province_id}/cities",
    response_model=list[CityResponse]
)
def read_cities(
    province_id: int,
    db: Session = Depends(get_db)
):
    return list_cities_by_province(
        db=db,
        province_id=province_id
    )