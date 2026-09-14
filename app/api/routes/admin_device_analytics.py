from fastapi import APIRouter, Depends


from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.device_analytics_service import (

    get_device_dashboard_summary,

    get_platform_statistics,

    get_version_statistics

)


from app.services.device_error_analytics_service import (

    get_device_error_dashboard

)



router = APIRouter(

    prefix="/admin/devices",

    tags=["Admin Device Analytics"]

)





@router.get("/analytics")
def device_analytics_dashboard(

    db: Session = Depends(get_db)

):


    summary = get_device_dashboard_summary(

        db

    )


    platforms = get_platform_statistics(

        db

    )


    versions = get_version_statistics(

        db

    )


    error_data = get_device_error_dashboard(

        db

    )



    return {


        **summary,


        "platforms": platforms,


        "versions": versions,


        "top_error_devices":

            error_data["top_error_devices"],


        "problematic_versions":

            error_data["problematic_versions"]

    }