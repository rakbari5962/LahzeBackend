from pydantic import BaseModel
from datetime import datetime


class OpportunityCreate(BaseModel):
    business_id: int
    service_id: int

    start_time: datetime
    end_time: datetime

    original_price: int
    discount_percent: int
    final_price: int

    capacity: int


class OpportunityResponse(BaseModel):
    id: int

    business_id: int
    service_id: int

    start_time: datetime
    end_time: datetime

    original_price: int
    discount_percent: int
    final_price: int

    capacity: int
    status: str

    class Config:
        from_attributes = True