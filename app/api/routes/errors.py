from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.error_report_service import (
    submit_error_report
)



router = APIRouter(

    prefix="/errors",

    tags=["Errors"]

)




@router.post("/report")
def create_error_report_request(

    occurrence_id: int,

    user_message: str | None = None,

    db: Session = Depends(get_db)

):


    return submit_error_report(

        db=db,

        occurrence_id=occurrence_id,

        user_message=user_message

    )