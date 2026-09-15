from datetime import datetime

from pydantic import BaseModel


class ReleaseItem(BaseModel):

    reward_event_id: int

    user_id: int

    booking_id: int

    amount: int

    type: str

    status: str

    transaction_id: str | None

    created_at: datetime



class ReleaseHistoryResponse(BaseModel):

    count: int

    items: list[ReleaseItem]