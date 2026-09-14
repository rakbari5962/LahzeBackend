from sqlalchemy.orm import Session


from app.models.error_report import ErrorReport





def create_error_report(
    db: Session,
    occurrence_id: int,
    system_description: str = None,
    user_message: str = None
):


    report = ErrorReport(

        occurrence_id=occurrence_id,

        system_description=system_description,

        user_message=user_message,

        status="OPEN"

    )


    db.add(report)

    db.commit()

    db.refresh(report)


    return report






def get_error_report(
    db: Session,
    report_id: int
):


    return db.query(
        ErrorReport
    ).filter(

        ErrorReport.id == report_id

    ).first()






def get_reports_by_occurrence(
    db: Session,
    occurrence_id: int
):


    return db.query(
        ErrorReport
    ).filter(

        ErrorReport.occurrence_id == occurrence_id

    ).all()






def update_error_report_status(
    db: Session,
    report_id: int,
    status: str
):


    report = get_error_report(
        db,
        report_id
    )


    if not report:

        return None



    report.status = status


    db.commit()

    db.refresh(report)


    return report