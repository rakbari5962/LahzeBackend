from pydantic import BaseModel


class BusinessProfileUpdate(BaseModel):
    description: str | None = None
    phone: str | None = None
    province_id: int | None = None
    city_id: int | None = None