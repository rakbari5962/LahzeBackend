from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import SessionLocal


from app.core.security.admin_guard import (
    admin_required
)


from app.schemas.admin_treasury_schema import (
    TreasuryHealthResponse
)


from app.services.admin_treasury_service import (
    get_treasury_health
)





router = APIRouter(

    prefix="/admin/dashboard",

    tags=["Admin Treasury"]

)





# --------------------------------------------------
# Database Dependency
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()





# --------------------------------------------------
# Treasury Health
# --------------------------------------------------

@router.get(
    "/treasury",
    response_model=TreasuryHealthResponse
)
def treasury_health(

    db: Session = Depends(get_db),

    admin = Depends(admin_required)

):

    return get_treasury_health(
        db
    )