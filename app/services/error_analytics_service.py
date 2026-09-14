from sqlalchemy.orm import Session


from app.repositories.error_analytics_repository import (

    get_total_errors,

    get_errors_by_status,

    get_top_errors,

    get_errors_by_severity,

    get_device_error_stats,

    get_version_error_stats

)


from app.repositories.error_repository import (
    get_error_definition
)





def get_dashboard_summary(
    db: Session
):


    total_errors = get_total_errors(
        db
    )


    status_summary = get_errors_by_status(
        db
    )


    severity_summary = get_errors_by_severity(
        db
    )



    return {


        "total_errors":
            total_errors,


        "status": {

            status: count

            for status, count in status_summary

        },


        "severity": {

            severity: count

            for severity, count in severity_summary

        }


    }








def get_top_error_list(
    db: Session,
    limit: int = 10
):


    errors = get_top_errors(

        db,

        limit

    )



    result = []



    for error_code, count in errors:


        definition = get_error_definition(

            db=db,

            error_code=error_code

        )


        result.append(

            {

                "error_code":
                    error_code,


                "name":
                    definition.name
                    if definition
                    else None,


                "severity":
                    definition.severity
                    if definition
                    else None,


                "count":
                    count

            }

        )



    return result







def get_device_statistics(
    db: Session
):


    results = get_device_error_stats(
        db
    )


    return [

        {

            "device_model":
                device_model,

            "count":
                count

        }

        for device_model, count in results

    ]









def get_version_statistics(
    db: Session
):


    results = get_version_error_stats(
        db
    )


    return [

        {

            "app_version":
                app_version,

            "count":
                count

        }

        for app_version, count in results

    ]