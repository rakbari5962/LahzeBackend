from sqlalchemy.orm import Session


from app.models.error_definition import (
    ErrorDefinition
)

from app.models.error_occurrence import (
    ErrorOccurrence
)

from app.models.error_report import (
    ErrorReport
)



# گرفتن تعریف یک خطا بر اساس کد

def get_error_definition(
    db: Session,
    error_code: int
):

    return db.query(
        ErrorDefinition
    ).filter(
        ErrorDefinition.error_code == error_code
    ).first()



# ثبت رخداد خطا

def create_error_occurrence(
    db: Session,
    error_code: int,
    user_id: int = None,
    action: str = None,
    device_info: dict = None,
    context: dict = None
):

    occurrence = ErrorOccurrence(

        error_code=error_code,

        user_id=user_id,

        action=action,

        device_info=device_info,

        context=context

    )


    db.add(
        occurrence
    )

    db.commit()

    db.refresh(
        occurrence
    )


    return occurrence



# ثبت گزارش کاربر برای ادمین

def create_error_report(
    db: Session,
    occurrence_id: int,
    user_message: str = None
):

    report = ErrorReport(

        occurrence_id=occurrence_id,

        user_message=user_message,

        status="OPEN"

    )


    db.add(
        report
    )

    db.commit()

    db.refresh(
        report
    )


    return report