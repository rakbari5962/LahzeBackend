from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import SessionLocal


from app.core.security.admin_guard import (
    admin_required
)


from app.schemas.admin_release_schema import (
    ReleaseHistoryResponse
)


from app.services.admin_release_service import (
    get_release_history_admin
)





router = APIRouter(

    prefix="/admin/dashboard",

    tags=["Admin Release History"]

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
# Release History
# --------------------------------------------------

@router.get(
    "/releases",
    response_model=ReleaseHistoryResponse
)
def release_history(

    db: Session = Depends(get_db),

    admin = Depends(admin_required)

):

    return get_release_history_admin(
        db
    )