from sqlalchemy.orm import Session


from app.models.error_report import ErrorReport

from app.models.error_occurrence import ErrorOccurrence

from app.models.error_definition import ErrorDefinition





def get_all_error_reports(
    db: Session
):


    return db.query(

        ErrorReport

    ).order_by(

        ErrorReport.id.desc()

    ).all()







def get_error_report_details(
    db: Session,
    report_id: int
):


    return db.query(

        ErrorReport

    ).filter(

        ErrorReport.id == report_id

    ).first()







def get_error_report_with_details(
    db: Session,
    report_id: int
):


    result = db.query(

        ErrorReport,
        ErrorOccurrence,
        ErrorDefinition

    ).join(

        ErrorOccurrence,

        ErrorReport.occurrence_id ==
        ErrorOccurrence.id

    ).join(

        ErrorDefinition,

        ErrorOccurrence.error_code ==
        ErrorDefinition.error_code

    ).filter(

        ErrorReport.id == report_id

    ).first()



    return result







def update_error_report_status(
    db: Session,
    report_id: int,
    status: str
):


    report = get_error_report_details(

        db,

        report_id

    )



    if not report:

        return None




    report.status = status



    db.commit()


    db.refresh(report)



    return report







def add_admin_note(
    db: Session,
    report_id: int,
    admin_note: str
):


    report = get_error_report_details(

        db,

        report_id

    )



    if not report:

        return None




    report.admin_note = admin_note



    db.commit()


    db.refresh(report)



    return report