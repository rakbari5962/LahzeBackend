from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import SessionLocal


from app.core.security.admin_guard import admin_required


from app.schemas.admin_dashboard_schema import (
    DashboardSummaryResponse
)


from app.services.admin_dashboard_service import (
    get_dashboard_summary
)





router = APIRouter(

    prefix="/admin/dashboard",

    tags=["Admin Dashboard"]

)





def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()





@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def dashboard_summary(

    db: Session = Depends(get_db),

    admin = Depends(admin_required)

):

    return get_dashboard_summary(
        db
    )