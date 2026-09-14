from app.database.database import Base, engine

from app.models.user_device import UserDevice



def create_user_device_table():


    print(
        "CREATING USER DEVICE TABLE"
    )

    print(
        "========================="
    )


    Base.metadata.create_all(
        bind=engine
    )


    print()

    print(
        "USER DEVICE TABLE CREATED ✅"
    )



if __name__ == "__main__":

    create_user_device_table()