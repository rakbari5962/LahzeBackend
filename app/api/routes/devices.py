from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.services.device_service import (

    register_or_update_device,

    get_user_devices,

    logout_device

)



router = APIRouter(

    prefix="/devices",

    tags=["Devices"]

)



@router.post("/register")
def register_device(

    user_id: int,

    device_id: str,

    platform: str,

    device_model: str | None = None,

    os_version: str | None = None,

    app_version: str | None = None,

    push_token: str | None = None,

    db: Session = Depends(get_db)

):


    device = register_or_update_device(

        db=db,

        user_id=user_id,

        device_id=device_id,

        platform=platform,

        device_model=device_model,

        os_version=os_version,

        app_version=app_version,

        push_token=push_token

    )


    return {

        "id": device.id,

        "device_id": device.device_id,

        "platform": device.platform,

        "app_version": device.app_version,

        "is_active": device.is_active

    }





@router.get("/me")
def my_devices(

    user_id: int,

    db: Session = Depends(get_db)

):


    devices = get_user_devices(

        db,

        user_id

    )


    return [

        {

            "id": device.id,

            "device_id": device.device_id,

            "platform": device.platform,

            "device_model": device.device_model,

            "app_version": device.app_version,

            "is_active": device.is_active

        }

        for device in devices

    ]





@router.patch("/{device_id}/logout")
def logout_user_device(

    device_id: str,

    db: Session = Depends(get_db)

):


    device = logout_device(

        db,

        device_id

    )


    return {

        "success": True,

        "device_id": device.device_id,

        "is_active": device.is_active

    }