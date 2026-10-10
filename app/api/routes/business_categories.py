from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.business_category_repository import get_categories
from app.schemas.business_category import BusinessCategoryResponse

router = APIRouter(prefix="/business-categories", tags=["Business Categories"])


@router.get("/", response_model=list[BusinessCategoryResponse])
def list_business_categories(db: Session = Depends(get_db)):
    """List active categories from the existing database table."""
    return get_categories(db)
