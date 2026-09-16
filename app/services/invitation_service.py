from sqlalchemy.orm import Session


from app.repositories.invitation_repository import (
    create_invitation
)


from app.schemas.invitation import InvitationCreate




def create_new_invitation(
    db: Session,
    inviter_user_id: int,
    data: InvitationCreate
):

    return create_invitation(

        db=db,

        inviter_user_id=inviter_user_id,

        owner_phone=data.owner_phone,

        business_name=data.business_name,

        city=data.city

    )