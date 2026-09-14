from sqlalchemy.orm import Session


from app.models.error_occurrence import ErrorOccurrence


from app.services.error_description_service import (
    generate_error_description
)


from app.repositories.error_report_repository import (
    create_error_report
)





def submit_error_report(
    db: Session,
    occurrence_id: int,
    user_message: str = None
):


    occurrence = db.query(
        ErrorOccurrence
    ).filter(

        ErrorOccurrence.id == occurrence_id

    ).first()



    if not occurrence:

        return None




    system_description = generate_error_description(
        db=db,
        occurrence_id=occurrence_id
    )




    report = create_error_report(

        db=db,

        occurrence_id=occurrence_id,

        system_description=system_description,

        user_message=user_message

    )



    if not report:

        return None




    return {

        "report_id": report.id,

        "occurrence_id": report.occurrence_id,

        "status": report.status,

        "system_description":
            report.system_description

    }