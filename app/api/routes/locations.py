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


@router.get("/cities/{city_id}/map-center")
def read_city_map_center(city_id: int, db=Depends(get_db)):
    """Return only an approved map center for a city."""
    from fastapi import HTTPException
    from sqlalchemy import text

    # Verify that the city exists.
    city_exists = db.execute(
        text("SELECT 1 FROM cities WHERE id = :city_id"),
        {"city_id": city_id},
    ).scalar()

    if city_exists is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    # Check whether the approved-coordinate table exists.
    has_approved = db.execute(
        text(
            "SELECT to_regclass('city_map_centers') IS NOT NULL"
        )
    ).scalar()

    # Never fall back to unapproved candidates or city-table coordinates.
    if not has_approved:
        return {
            "city_id": city_id,
            "latitude": None,
            "longitude": None,
            "coordinate_status": "NO_APPROVED_COORDINATES",
        }

    row = db.execute(
        text("""
            SELECT latitude, longitude
            FROM city_map_centers
            WHERE city_id = :city_id
        """),
        {"city_id": city_id},
    ).mappings().first()

    if (
        row is None
        or row["latitude"] is None
        or row["longitude"] is None
    ):
        return {
            "city_id": city_id,
            "latitude": None,
            "longitude": None,
            "coordinate_status": "NO_APPROVED_COORDINATES",
        }

    return {
        "city_id": city_id,
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "coordinate_status": "APPROVED_FOR_MAP",
    }
