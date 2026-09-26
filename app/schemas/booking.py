from pydantic import BaseModel
from datetime import datetime


class BookingCreate(BaseModel):
    opportunity_id: int


class BusinessSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class OpportunitySummary(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    final_price: int

    class Config:
        from_attributes = True


class WalletHoldResponse(BaseModel):

    amount: int
    status: str
    created_at: datetime
    released_at: datetime | None = None

    class Config:
        from_attributes = True



class BookingResponse(BaseModel):

    id: int

    user_id: int
    business_id: int
    opportunity_id: int

    status: str

    created_at: datetime

    confirmed_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None


    business: BusinessSummary | None = None
    opportunity: OpportunitySummary | None = None
    wallet_hold: WalletHoldResponse | None = None


    class Config:
        from_attributes = True



class BookingCancelPreviewResponse(BaseModel):

    booking_id: int

    amount: int

    penalty_percent: int

    penalty_amount: int

    customer_refund: int

    requires_confirmation: bool = True