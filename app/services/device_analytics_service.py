from sqlalchemy.orm import Session


from app.repositories.device_analytics_repository import (

    get_total_active_devices,

    get_devices_by_platform,

    get_devices_by_app_version

)





def get_device_dashboard_summary(
    db: Session
):


    total_active_devices = get_total_active_devices(

        db

    )


    return {

        "total_active_devices": total_active_devices

    }





def get_platform_statistics(
    db: Session
):


    results = get_devices_by_platform(

        db

    )


    return [

        {

            "platform": platform,

            "count": count

        }

        for platform, count in results

    ]





def get_version_statistics(
    db: Session
):


    results = get_devices_by_app_version(

        db

    )


    return [

        {

            "app_version": version,

            "count": count

        }

        for version, count in results

    ]