from pydantic import BaseModel


class CityResponse(BaseModel):
    id: int
    name: str
    province_id: int

    class Config:
        from_attributes = True