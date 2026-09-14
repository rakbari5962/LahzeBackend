from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.business_category_suggestion import (
    BusinessCategorySuggestionRequest,
    BusinessCategorySuggestionResponse
)


from app.services.category_ai_service import (
    suggest_business_category
)



router = APIRouter(

    prefix="/businesses",

    tags=["Business Category AI"]

)



@router.post(
    "/suggest-category",
    response_model=BusinessCategorySuggestionResponse
)
def suggest_category(

    data: BusinessCategorySuggestionRequest,

    db: Session = Depends(get_db)

):

    return suggest_business_category(

        db=db,

        name=data.name,

        description=data.description,

        services=data.services

    )