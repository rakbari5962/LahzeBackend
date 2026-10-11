from pydantic import BaseModel, Field







class BusinessCreate(BaseModel):

    name: str

    category_id: int | None = None

    # A new category title the user confirmed; mutually exclusive with
    # category_id. Quarantined for admin review, never a category by itself.
    proposed_category_title: str | None = Field(

        default=None,

        max_length=60

    )

    province_id: int

    city_id: int

    services: list[str] = Field(

        default_factory=list

    )

    description: str | None = None

    phone: str | None = None










class BusinessLocationUpdate(BaseModel):
    province_id: int
    city_id: int
    latitude: float
    longitude: float
    address: str | None = None



class BusinessResponse(BaseModel):

    id: int

    name: str

    category_id: int | None = None

    owner_user_id: int

    province_id: int | None = None

    city_id: int | None = None

    latitude: float | None = None

    longitude: float | None = None

    address: str | None = None

    description: str | None = None

    phone: str | None = None

    status: str | None = None

    category_pending: bool = False

    proposal_id: int | None = None



    class Config:

        from_attributes = True