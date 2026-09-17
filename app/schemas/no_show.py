from pydantic import BaseModel

from datetime import datetime



class NoShowReportResponse(BaseModel):

    id: int

    booking_id: int

    business_id: int

    status: str

    reported_at: datetime | None = None

    customer_response_at: datetime | None = None

    resolved_at: datetime | None = None



    class Config:

        from_attributes = True