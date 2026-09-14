from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.core.security.permissions import require_admin


from app.services.error_analytics_service import (

    get_dashboard_summary,

    get_top_error_list,

    get_device_statistics,

    get_version_statistics

)





router = APIRouter(

    prefix="/admin/errors/analytics",

    tags=["Admin Error Analytics"]

)





@router.get("/")

def dashboard(

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return get_dashboard_summary(

        db

    )







@router.get("/top")

def top_errors(

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return get_top_error_list(

        db

    )







@router.get("/devices")

def device_statistics(

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return get_device_statistics(

        db

    )







@router.get("/versions")

def version_statistics(

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return get_version_statistics(

        db

    )