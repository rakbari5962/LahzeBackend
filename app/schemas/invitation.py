from pydantic import BaseModel

from datetime import datetime


class InvitationCreate(BaseModel):

    owner_phone: str

    business_name: str | None = None

    city: str | None = None



class InvitationResponse(BaseModel):

    id: int

    inviter_user_id: int

    owner_phone: str

    business_name: str | None

    city: str | None

    status: str

    accepted_user_id: int | None

    created_at: datetime


    class Config:

        from_attributes = True