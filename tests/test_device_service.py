from app.database.database import SessionLocal


from app.models.user import User


from app.models.user_device import UserDevice


from app.services.device_service import (

    register_or_update_device,

    get_user_devices,

    logout_device

)





def test_device_service():


    print(
        "DEVICE SERVICE TEST"
    )

    print(
        "=================="
    )



    db = SessionLocal()



    # 1) CREATE USER


    user = User(

        phone_number="09990000002",

        role="CUSTOMER"

    )


    db.add(user)

    db.commit()

    db.refresh(user)



    print()

    print(
        "USER CREATED:",
        user.id
    )





    # 2) FIRST DEVICE REGISTER


    device = register_or_update_device(

        db=db,

        user_id=user.id,

        device_id="SERVICE_DEVICE_001",

        platform="ANDROID",

        device_model="Galaxy A54",

        os_version="Android 15",

        app_version="1.0.7"

    )



    print()

    print(
        "FIRST REGISTER:",
        device.id,
        device.app_version
    )



    assert device.app_version == "1.0.7"





    # 3) REGISTER SAME DEVICE AGAIN


    updated_device = register_or_update_device(

        db=db,

        user_id=user.id,

        device_id="SERVICE_DEVICE_001",

        platform="ANDROID",

        device_model="Galaxy A54",

        os_version="Android 15",

        app_version="1.0.8"

    )



    print()

    print(
        "SECOND REGISTER:",
        updated_device.id,
        updated_device.app_version
    )



    assert updated_device.id == device.id

    assert updated_device.app_version == "1.0.8"





    # 4) VERIFY NO DUPLICATE


    count = db.query(

        UserDevice

    ).filter(

        UserDevice.device_id == "SERVICE_DEVICE_001"

    ).count()



    print()

    print(
        "DEVICE COUNT:",
        count
    )



    assert count == 1





    # 5) GET ACTIVE DEVICES


    devices = get_user_devices(

        db,

        user.id

    )


    print()

    print(
        "ACTIVE DEVICES:",
        len(devices)
    )



    assert len(devices) == 1





    # 6) LOGOUT


    logged_out = logout_device(

        db,

        "SERVICE_DEVICE_001"

    )



    print()

    print(
        "LOGOUT STATUS:",
        logged_out.is_active
    )



    assert logged_out.is_active is False





    # 7) VERIFY ACTIVE LIST EMPTY


    devices_after_logout = get_user_devices(

        db,

        user.id

    )


    print()

    print(
        "ACTIVE AFTER LOGOUT:",
        len(devices_after_logout)
    )



    assert len(devices_after_logout) == 0





    # CLEANUP


    db.delete(user)

    db.commit()

    db.close()



    print()

    print(
        "DEVICE SERVICE PASSED ✅"
    )





if __name__ == "__main__":

    test_device_service()