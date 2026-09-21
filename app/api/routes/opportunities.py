from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityResponse
)

from app.repositories.opportunity_repository import (
    create_opportunity,
    get_opportunity,
    get_active_opportunities,
    get_business_opportunities
)


router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.post(
    "/",
    response_model=OpportunityResponse
)
def create_new_opportunity(
    opportunity: OpportunityCreate,
    db: Session = Depends(get_db)
):
    return create_opportunity(
        db,
        opportunity
    )


@router.get(
    "/",
    response_model=list[OpportunityResponse]
)
def read_active_opportunities(
    db: Session = Depends(get_db)
):
    return get_active_opportunities(db)


@router.get(
    "/{opportunity_id}",
    response_model=OpportunityResponse
)
def read_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db)
):
    return get_opportunity(
        db,
        opportunity_id
    )

@router.get(
    "/business/{business_id}",
    response_model=list[OpportunityResponse]
)
def read_business_opportunities(
    business_id: int,
    db: Session = Depends(get_db)
):
    return get_business_opportunities(
        db,
        business_id
    )