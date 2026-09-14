from pydantic import BaseModel



class BusinessCategoryCreate(BaseModel):

    name: str

    slug: str

    description: str | None = None





class BusinessCategoryResponse(BaseModel):

    id: int

    name: str

    slug: str

    description: str | None = None

    is_active: bool


    class Config:

        from_attributes = True