from datetime import datetime

from pydantic import BaseModel





class ReleaseErrorItem(BaseModel):

    reward_event_id: int

    user_id: int

    booking_id: int

    amount: int

    type: str

    status: str

    transaction_id: str | None

    created_at: datetime





class ReleaseErrorsResponse(BaseModel):

    count: int

    items: list[ReleaseErrorItem]