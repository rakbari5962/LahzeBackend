from pydantic import BaseModel


class ServiceCreate(BaseModel):
    business_id: int
    name: str
    base_price: int
    duration_minutes: int


class ServiceResponse(BaseModel):
    id: int
    business_id: int
    name: str
    base_price: int
    duration_minutes: int
    active: bool

    class Config:
        from_attributes = True