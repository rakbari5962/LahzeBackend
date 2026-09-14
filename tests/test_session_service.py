from app.database.database import SessionLocal

from app.services.session_service import (
    create_login_session,
    get_login_session,
    logout
)

from app.models.user import User





def test_session_service():

    print(
        "SESSION SERVICE TEST"
    )

    print(
        "==================="
    )


    db = SessionLocal()


    # پیدا کردن یک کاربر تستی
    user = (

        db.query(User)

        .filter(
            User.phone_number == "09129367314"
        )

        .first()

    )


    assert user is not None


    print()

    print(
        "USER:"
    )

    print(
        user.id,
        user.phone_number
    )



    # ساخت Login Session

    session = create_login_session(

        db=db,

        user_id=user.id

    )


    print()

    print(
        "SESSION CREATED:"
    )

    print(
        session.id
    )

    print(
        session.token
    )



    assert session.user_id == user.id

    assert session.is_active is True



    # پیدا کردن Session با Token

    found_session = get_login_session(

        db=db,

        token=session.token

    )


    print()

    print(
        "SESSION FOUND:"
    )

    print(
        found_session.id
    )


    assert found_session is not None

    assert found_session.token == session.token



    # Logout

    logout(

        db=db,

        session=found_session

    )


    print()

    print(
        "LOGOUT DONE"
    )



    db.refresh(
        found_session
    )


    assert found_session.is_active is False



    db.close()



    print()

    print(
        "SESSION SERVICE PASSED ✅"
    )





if __name__ == "__main__":

    test_session_service()