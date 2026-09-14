from sqlalchemy.orm import Session


from app.repositories.device_repository import (

    get_device_by_device_id,

    create_device,

    update_device,

    get_active_user_devices,

    deactivate_device

)





def register_or_update_device(

    db: Session,

    user_id: int,

    device_id: str,

    platform: str,

    device_model: str = None,

    os_version: str = None,

    app_version: str = None,

    push_token: str = None

):


    existing_device = get_device_by_device_id(

        db,

        device_id

    )



    if existing_device:


        return update_device(

            db=db,

            device=existing_device,

            user_id=user_id,

            platform=platform,

            device_model=device_model,

            os_version=os_version,

            app_version=app_version,

            push_token=push_token

        )



    return create_device(

        db=db,

        user_id=user_id,

        device_id=device_id,

        platform=platform,

        device_model=device_model,

        os_version=os_version,

        app_version=app_version,

        push_token=push_token

    )







def get_user_devices(

    db: Session,

    user_id: int

):


    return get_active_user_devices(

        db,

        user_id

    )







def logout_device(

    db: Session,

    device_id: str

):


    return deactivate_device(

        db,

        device_id

    )