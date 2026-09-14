from sqlalchemy.orm import Session


from app.repositories.error_repository import (
    get_error_definition,
    create_error_occurrence
)



def record_error(
    db: Session,
    error_code: int,
    action: str = None,
    user_id: int = None,
    device_info: dict = None,
    context: dict = None
):


    # پیدا کردن تعریف خطا

    error_definition = get_error_definition(
        db=db,
        error_code=error_code
    )


    if not error_definition:

        raise Exception(
            f"UNKNOWN ERROR CODE: {error_code}"
        )



    # ثبت رخداد خطا

    occurrence = create_error_occurrence(
        db=db,
        error_code=error_code,
        user_id=user_id,
        action=action,
        device_info=device_info,
        context=context
    )



    return {

        "error_code": error_code,

        "name": error_definition.name,

        "severity": error_definition.severity,

        "occurrence_id": occurrence.id

    }