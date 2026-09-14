from pydantic import BaseModel



class BusinessServiceCreate(BaseModel):

    name: str

    category: str | None = None

    duration_minutes: int | None = None

    price: int | None = None

    description: str | None = None





class BusinessServiceResponse(BaseModel):

    id: int

    business_id: int

    name: str

    category: str | None = None

    duration_minutes: int | None = None

    price: int | None = None

    description: str | None = None

    is_active: bool


    class Config:

        from_attributes = True