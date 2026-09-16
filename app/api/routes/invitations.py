from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session


from app.database.dependencies import get_db


from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse
)


from app.services.invitation_service import (
    create_new_invitation
)


from app.services.session_service import (
    get_login_session
)



router = APIRouter(

    prefix="/invitations",

    tags=["Invitations"]

)





@router.post(

    "/",

    response_model=InvitationResponse

)
def create_invitation_route(

    data: InvitationCreate,

    token: str = Query(...),

    db: Session = Depends(get_db)

):


    session = get_login_session(

        db=db,

        token=token

    )


    if not session:

        raise Exception(

            "User not logged in"

        )


    return create_new_invitation(

        db=db,

        inviter_user_id=session.user_id,

        data=data

    )