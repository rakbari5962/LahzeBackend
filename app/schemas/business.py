from pydantic import BaseModel, Field







class BusinessCreate(BaseModel):

    name: str

    province_id: int

    city_id: int

    services: list[str] = Field(

        default_factory=list

    )

    description: str | None = None

    phone: str | None = None










class BusinessLocationUpdate(BaseModel):

    latitude: float

    longitude: float

    address: str | None = None










class BusinessResponse(BaseModel):

    id: int

    name: str

    owner_user_id: int

    province_id: int

    city_id: int

    latitude: float | None = None

    longitude: float | None = None

    address: str | None = None

    description: str | None = None

    phone: str | None = None

    status: str | None = None



    class Config:

        from_attributes = True