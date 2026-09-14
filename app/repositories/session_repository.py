from sqlalchemy.orm import Session

from app.models.session import Session as UserSession





def create_session(

    db: Session,

    user_id: int,

    token: str,

    expires_at,

    is_temporary: bool = False

):


    session = UserSession(

        user_id=user_id,

        token=token,

        expires_at=expires_at,

        is_active=True,

        is_temporary=is_temporary

    )


    db.add(session)

    db.commit()

    db.refresh(session)


    return session











def get_session_by_token(

    db: Session,

    token: str

):


    return (

        db.query(UserSession)

        .filter(

            UserSession.token == token,

            UserSession.is_active == True

        )

        .first()

    )












def logout_session(

    db: Session,

    session: UserSession

):


    session.is_active = False


    db.commit()

    db.refresh(session)


    return session












def complete_session(

    db: Session,

    session: UserSession

):


    session.is_temporary = False


    db.commit()

    db.refresh(session)


    return session