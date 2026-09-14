from sqlalchemy.orm import Session


from app.repositories.device_error_analytics_repository import (

    get_errors_by_device_model,

    get_errors_by_device_version

)





def get_device_error_statistics(
    db: Session
):


    results = get_errors_by_device_model(

        db

    )


    return [

        {

            "device_model": device_model,

            "error_count": count

        }

        for device_model, count in results

    ]





def get_version_error_statistics(
    db: Session
):


    results = get_errors_by_device_version(

        db

    )


    return [

        {

            "app_version": app_version,

            "error_count": count

        }

        for app_version, count in results

    ]





def get_device_error_dashboard(
    db: Session
):


    return {

        "top_error_devices":
            get_device_error_statistics(
                db
            ),


        "problematic_versions":
            get_version_error_statistics(
                db
            )

    }