from pydantic import BaseModel


class CityResponse(BaseModel):
    id: int
    name: str
    province_id: int
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        from_attributes = True