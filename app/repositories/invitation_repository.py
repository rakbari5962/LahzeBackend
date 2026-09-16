from sqlalchemy.orm import Session

from app.models.invitation import Invitation


def create_invitation(
    db: Session,
    inviter_user_id: int,
    owner_phone: str,
    business_name: str | None = None,
    city: str | None = None
):

    invitation = Invitation(

        inviter_user_id=inviter_user_id,

        owner_phone=owner_phone,

        business_name=business_name,

        city=city,

        status="PENDING"

    )


    db.add(invitation)

    db.commit()

    db.refresh(invitation)


    return invitation



def get_invitation(
    db: Session,
    invitation_id: int
):

    return (

        db.query(Invitation)

        .filter(

            Invitation.id == invitation_id

        )

        .first()

    )



def accept_invitation(
    db: Session,
    invitation: Invitation,
    user_id: int,
    user_phone: str
):

    invitation.accepted_user_id = user_id

    invitation.status = "ACCEPTED"


    invitation.accepted_phone_match = (
        invitation.owner_phone == user_phone
    )


    db.commit()

    db.refresh(invitation)


    return invitation