from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.business_category_suggestion import (
    BusinessCategorySuggestionRequest,
    BusinessCategorySuggestionResponse,
)
from app.services.category_resolution_service import resolve_category

router = APIRouter(prefix="/businesses", tags=["Business Category Suggestions"])


@router.post("/suggest-category", response_model=BusinessCategorySuggestionResponse)
def suggest_category(
    data: BusinessCategorySuggestionRequest,
    db: Session = Depends(get_db),
):
    """Suggest a category before Business creation.

    Resolves against existing categories and managed aliases first and only then
    asks the LLM for a new title. Never writes to the database.
    """
    return resolve_category(
        db=db,
        business_name=data.name,
        services=data.services,
        description=data.description,
    )
