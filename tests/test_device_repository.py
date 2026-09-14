from datetime import datetime


from app.database.database import SessionLocal


from app.models.user import User


from app.models.user_device import UserDevice


from app.repositories.device_repository import (

    get_device_by_device_id,

    create_device,

    update_device,

    get_active_user_devices,

    deactivate_device

)





def test_device_repository():


    print(
        "DEVICE REPOSITORY TEST"
    )

    print(
        "====================="
    )



    db = SessionLocal()



    # 1) CREATE TEST USER


    user = User(

        phone_number="09990000001",

        role="CUSTOMER"

    )


    db.add(
        user
    )

    db.commit()

    db.refresh(
        user
    )



    print()

    print(
        "USER CREATED:",
        user.id
    )





    # 2) CREATE DEVICE


    device = create_device(

        db=db,

        user_id=user.id,

        device_id="TEST_DEVICE_001",

        platform="ANDROID",

        device_model="Galaxy A54",

        os_version="Android 15",

        app_version="1.0.7"

    )



    print()

    print(
        "DEVICE CREATED:",
        device.id
    )



    assert device.device_id == "TEST_DEVICE_001"





    # 3) FIND DEVICE


    found_device = get_device_by_device_id(

        db,

        "TEST_DEVICE_001"

    )


    print()

    print(
        "DEVICE FOUND:",
        found_device.device_id
    )



    assert found_device.id == device.id





    # 4) UPDATE DEVICE


    updated_device = update_device(

        db=db,

        device=device,

        user_id=user.id,

        app_version="1.0.8",

        os_version="Android 16"

    )


    print()

    print(
        "DEVICE UPDATED:",
        updated_device.app_version
    )


    assert updated_device.app_version == "1.0.8"

    assert updated_device.os_version == "Android 16"





    # 5) GET ACTIVE DEVICES


    active_devices = get_active_user_devices(

        db,

        user.id

    )


    print()

    print(
        "ACTIVE DEVICES:",
        len(active_devices)
    )


    assert len(active_devices) == 1





    # 6) DEACTIVATE DEVICE


    deactivated = deactivate_device(

        db,

        "TEST_DEVICE_001"

    )


    print()

    print(
        "DEVICE ACTIVE STATUS:",
        deactivated.is_active
    )


    assert deactivated.is_active is False





    # 7) VERIFY


    active_devices_after = get_active_user_devices(

        db,

        user.id

    )


    print()

    print(
        "ACTIVE DEVICES AFTER DEACTIVATE:",
        len(active_devices_after)
    )


    assert len(active_devices_after) == 0



    db.delete(
        user
    )

    db.commit()



    db.close()



    print()

    print(
        "DEVICE REPOSITORY PASSED ✅"
    )





if __name__ == "__main__":

    test_device_repository()