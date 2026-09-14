from pydantic import BaseModel


class UserCreate(BaseModel):

    phone_number: str
    province_id: int | None = None
    city_id: int | None = None



class UserCityUpdate(BaseModel):

    city_id: int
    province_id: int | None = None



class UserResponse(BaseModel):

    id: int
    phone_number: str
    province_id: int | None = None
    city_id: int | None = None

    class Config:
        from_attributes = True