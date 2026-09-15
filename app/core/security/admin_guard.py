from fastapi import (
    Depends,
    HTTPException,
    Header
)

from sqlalchemy.orm import Session


from app.database.database import SessionLocal

from app.models.user import User

from app.services.session_service import (
    get_login_session
)





# --------------------------------------------------
# Database Dependency
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()





# --------------------------------------------------
# دریافت User از Session Token
# --------------------------------------------------

def get_current_user(
    x_session_token: str = Header(
        ...,
        alias="X-Session-Token"
    ),
    db: Session = Depends(get_db)
):


    session = get_login_session(
        db=db,
        token=x_session_token
    )


    if not session:

        raise HTTPException(
            status_code=401,
            detail="Invalid session token"
        )



    user = db.query(
        User
    ).filter(
        User.id == session.user_id
    ).first()



    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user





# --------------------------------------------------
# فقط Admin
# --------------------------------------------------

def admin_required(
    current_user: User = Depends(get_current_user)
):


    if current_user.role != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


    return current_user