from app.models.user import User
from app.models.user_device import UserDevice

from app.database.database import Base



def test_user_device_model():

    print(
        "USER DEVICE MODEL TEST"
    )

    print(
        "====================="
    )


    print(
        "TABLES:"
    )

    print(
        Base.metadata.tables.keys()
    )


    assert "users" in Base.metadata.tables

    assert "user_devices" in Base.metadata.tables


    print()

    print(
        "USER DEVICE MODEL PASSED ✅"
    )



if __name__ == "__main__":

    test_user_device_model()