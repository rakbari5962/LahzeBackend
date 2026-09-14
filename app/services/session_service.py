import secrets

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session


from app.repositories.session_repository import (
    create_session,
    get_session_by_token,
    logout_session
)


# مدت نگهداری وضعیت Login
SESSION_EXPIRE_DAYS = 30



def generate_token():

    return secrets.token_urlsafe(32)




def create_login_session(

    db: Session,

    user_id: int,

    is_temporary: bool = False

):

    token = generate_token()


    expires_at = (

        datetime.now(timezone.utc)

        +

        timedelta(
            days=SESSION_EXPIRE_DAYS
        )

    )


    session = create_session(

        db=db,

        user_id=user_id,

        token=token,

        expires_at=expires_at,

        is_temporary=is_temporary

    )


    return session




def get_login_session(

    db: Session,

    token: str

):

    session = get_session_by_token(

        db=db,

        token=token

    )


    if not session:

        return None



    if not session.is_active:

        return None



    if session.expires_at < datetime.now(timezone.utc):

        return None



    return session




def is_session_active(

    db: Session,

    token: str

):

    session = get_login_session(

        db=db,

        token=token

    )


    return session is not None




def logout(

    db: Session,

    session

):

    if not session:

        return None


    return logout_session(

        db=db,

        session=session

    )