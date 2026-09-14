from sqlalchemy.orm import Session


from app.models.user_device import UserDevice





def get_device_by_device_id(
    db: Session,
    device_id: str
):

    return db.query(

        UserDevice

    ).filter(

        UserDevice.device_id == device_id

    ).first()





def create_device(
    db: Session,
    user_id: int,
    device_id: str,
    platform: str,
    device_model: str = None,
    os_version: str = None,
    app_version: str = None,
    push_token: str = None
):


    device = UserDevice(

        user_id=user_id,

        device_id=device_id,

        platform=platform,

        device_model=device_model,

        os_version=os_version,

        app_version=app_version,

        push_token=push_token

    )


    db.add(
        device
    )

    db.commit()

    db.refresh(
        device
    )


    return device





def update_device(
    db: Session,
    device: UserDevice,
    user_id: int,
    platform: str = None,
    device_model: str = None,
    os_version: str = None,
    app_version: str = None,
    push_token: str = None
):


    device.user_id = user_id


    if platform:
        device.platform = platform


    if device_model:
        device.device_model = device_model


    if os_version:
        device.os_version = os_version


    if app_version:
        device.app_version = app_version


    if push_token:
        device.push_token = push_token


    db.commit()

    db.refresh(
        device
    )


    return device





def get_active_user_devices(
    db: Session,
    user_id: int
):


    return db.query(

        UserDevice

    ).filter(

        UserDevice.user_id == user_id,

        UserDevice.is_active == True

    ).all()





def deactivate_device(
    db: Session,
    device_id: str
):


    device = get_device_by_device_id(

        db,

        device_id

    )


    if not device:

        return None



    device.is_active = False


    db.commit()

    db.refresh(
        device
    )


    return device