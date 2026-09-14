from sqlalchemy.orm import Session

from sqlalchemy import func


from app.models.user_device import UserDevice




def get_total_active_devices(
    db: Session
):

    return db.query(

        func.count(UserDevice.id)

    ).filter(

        UserDevice.is_active == True

    ).scalar()





def get_devices_by_platform(
    db: Session
):

    return (

        db.query(

            UserDevice.platform,

            func.count(UserDevice.id)

        )

        .group_by(

            UserDevice.platform

        )

        .all()

    )





def get_devices_by_app_version(
    db: Session
):

    return (

        db.query(

            UserDevice.app_version,

            func.count(UserDevice.id)

        )

        .group_by(

            UserDevice.app_version

        )

        .order_by(

            func.count(UserDevice.id).desc()

        )

        .all()

    )