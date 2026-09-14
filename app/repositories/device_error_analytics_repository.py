from sqlalchemy.orm import Session

from sqlalchemy import func, cast, String


from app.models.error_occurrence import ErrorOccurrence





def get_errors_by_device_model(
    db: Session
):


    device_model = func.trim(

        cast(

            ErrorOccurrence.device_info["device_model"],

            String

        ),

        '"'

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





def get_errors_by_device_version(
    db: Session
):


    app_version = func.trim(

        cast(

            ErrorOccurrence.device_info["app_version"],

            String

        ),

        '"'

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