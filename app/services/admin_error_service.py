from sqlalchemy.orm import Session


from app.repositories.admin_error_repository import (

    get_all_error_reports,

    get_error_report_with_details,

    update_error_report_status,

    add_admin_note

)





def list_error_reports(
    db: Session
):


    reports = get_all_error_reports(
        db
    )


    return [

        {

            "id": report.id,

            "occurrence_id":
                report.occurrence_id,

            "status":
                report.status,

            "user_message":
                report.user_message,

            "created_at":
                report.created_at

        }

        for report in reports

    ]








def get_error_details(
    db: Session,
    report_id: int
):


    result = get_error_report_with_details(

        db,

        report_id

    )


    if not result:

        return None



    report, occurrence, definition = result



    return {


        "report_id":
            report.id,


        "status":
            report.status,


        "user_message":
            report.user_message,


        "admin_note":
            report.admin_note,


        "system_description":
            report.system_description,


        "error": {


            "code":
                definition.error_code,


            "name":
                definition.name,


            "severity":
                definition.severity,


            "description":
                definition.description

        },


        "occurrence": {


            "action":
                occurrence.action,

            "device_info":
                occurrence.device_info,

            "context":
                occurrence.context

        

        }


    }








def change_error_status(
    db: Session,
    report_id: int,
    status: str
):


    allowed_statuses = [

        "OPEN",

        "INVESTIGATING",

        "RESOLVED"

    ]



    if status not in allowed_statuses:

        return None



    return update_error_report_status(

        db,

        report_id,

        status

    )








def write_admin_note(
    db: Session,
    report_id: int,
    note: str
):


    return add_admin_note(

        db,

        report_id,

        note

    )