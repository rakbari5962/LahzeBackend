from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import SessionLocal


from app.core.security.admin_guard import (
    admin_required
)


from app.schemas.admin_release_error_schema import (
    ReleaseErrorsResponse
)


from app.services.admin_release_error_service import (
    get_release_errors_admin
)





router = APIRouter(

    prefix="/admin/dashboard",

    tags=["Admin Release Errors"]

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
# Failed Release Errors
# --------------------------------------------------

@router.get(
    "/release-errors",
    response_model=ReleaseErrorsResponse
)
def release_errors(

    db: Session = Depends(get_db),

    admin = Depends(admin_required)

):

    return get_release_errors_admin(
        db
    )