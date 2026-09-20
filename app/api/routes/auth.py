from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.database import SessionLocal


from app.services.auth_service import (
    request_otp,
    verify_otp
)


from app.services.session_service import (
    get_login_session,
    logout
)


from app.models.user import User





router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)







def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()







@router.post("/request-otp")
def request_otp_code(

    phone_number: str,

    db: Session = Depends(get_db)

):

    request_otp(

        db=db,

        phone_number=phone_number

    )


    return {

        "success": True,

        "message": "OTP sent"

    }









@router.post("/verify-otp")
def verify_otp_code(

    phone_number: str,

    code: str,

    invitation_id: int | None = None,

    db: Session = Depends(get_db)

):

    result = verify_otp(

        db=db,

        phone_number=phone_number,

        code=code,

        invitation_id=invitation_id

    )


    user = result["user"]


    if result["requires_city_selection"]:

        session = result["session"]

        return {

            "success": True,

            "requires_city_selection": True,

            "user_id": user.id,

            "phone_number": user.phone_number,

            "session_token": session.token

        }






    session = result["session"]


    return {

        "success": True,

        "requires_city_selection": False,

        "user_id": user.id,

        "phone_number": user.phone_number,

        "session_token": session.token

    }









@router.get("/session")
def current_session(

    token: str,

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )



    if not session:


        return {

            "success": True,

            "logged_in": False

        }



    user = (

        db.query(User)

        .filter(

            User.id == session.user_id

        )

        .first()

    )



    return {

        "success": True,

        "logged_in": True,

        "user_id": user.id,

        "phone_number": user.phone_number

    }









@router.post("/logout")
def logout_user(

    token: str,

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )



    if not session:


        return {

            "success": True,

            "message": "Already logged out"

        }



    logout(

        db=db,

        session=session

    )



    return {

        "success": True,

        "message": "Logged out"

    }