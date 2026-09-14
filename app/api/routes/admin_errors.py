from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.core.security.permissions import require_admin


from app.services.admin_error_service import (

    list_error_reports,

    get_error_details,

    change_error_status,

    write_admin_note

)





router = APIRouter(

    prefix="/admin/errors",

    tags=["Admin Errors"]

)







@router.get("/")
def get_errors(

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return list_error_reports(

        db

    )










@router.get("/{report_id}")
def get_error(

    report_id: int,

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return get_error_details(

        db,

        report_id

    )










@router.patch("/{report_id}/status")
def update_error_status(

    report_id: int,

    status: str,

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return change_error_status(

        db,

        report_id,

        status

    )










@router.patch("/{report_id}/note")
def update_error_note(

    report_id: int,

    note: str,

    admin = Depends(require_admin),

    db: Session = Depends(get_db)

):

    return write_admin_note(

        db,

        report_id,

        note

    )