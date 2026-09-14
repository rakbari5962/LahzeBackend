from sqlalchemy.orm import Session

from sqlalchemy import func


from app.models.error_occurrence import ErrorOccurrence

from app.models.error_definition import ErrorDefinition

from app.models.error_report import ErrorReport





def get_total_errors(
    db: Session
):

    return db.query(
        func.count(ErrorOccurrence.id)
    ).scalar()







def get_errors_by_status(
    db: Session
):

    results = (

        db.query(

            ErrorReport.status,

            func.count(
                ErrorReport.id
            )

        )

        .group_by(

            ErrorReport.status

        )

        .all()

    )


    return results







def get_top_errors(
    db: Session,
    limit: int = 10
):

    results = (

        db.query(

            ErrorOccurrence.error_code,

            func.count(
                ErrorOccurrence.id
            ).label(
                "count"
            )

        )

        .group_by(

            ErrorOccurrence.error_code

        )

        .order_by(

            func.count(
                ErrorOccurrence.id
            ).desc()

        )

        .limit(

            limit

        )

        .all()

    )


    return results







def get_errors_by_severity(
    db: Session
):

    results = (

        db.query(

            ErrorDefinition.severity,

            func.count(
                ErrorOccurrence.id
            )

        )

        .join(

            ErrorOccurrence,

            ErrorOccurrence.error_code
            ==
            ErrorDefinition.error_code

        )

        .group_by(

            ErrorDefinition.severity

        )

        .all()

    )


    return results







def get_device_error_stats(
    db: Session
):


    device_model = func.json_extract_path_text(

        ErrorOccurrence.device_info,

        "device_model"

    )


    results = (

        db.query(

            device_model.label(
                "device_model"
            ),

            func.count(
                ErrorOccurrence.id
            ).label(
                "count"
            )

        )

        .group_by(

            device_model

        )

        .order_by(

            func.count(
                ErrorOccurrence.id
            ).desc()

        )

        .all()

    )


    return results







def get_version_error_stats(
    db: Session
):


    app_version = func.json_extract_path_text(

        ErrorOccurrence.device_info,

        "app_version"

    )


    results = (

        db.query(

            app_version.label(
                "app_version"
            ),

            func.count(
                ErrorOccurrence.id
            ).label(
                "count"
            )

        )

        .group_by(

            app_version

        )

        .order_by(

            func.count(
                ErrorOccurrence.id
            ).desc()

        )

        .all()

    )


    return results