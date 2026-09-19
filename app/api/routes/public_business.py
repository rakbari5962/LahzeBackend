from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.public_business_service import (
    get_public_business_profile
)

from app.schemas.public_business import (
    PublicBusinessProfileResponse
)



router = APIRouter(
    prefix="/businesses",
    tags=["Public Business"]
)



@router.get(
    "/{business_id}/public-profile",
    response_model=PublicBusinessProfileResponse
)
def public_business_profile(
    business_id: int,
    db: Session = Depends(get_db)
):

    result = get_public_business_profile(
        db=db,
        business_id=business_id
    )


    if not result:

        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )


    return result