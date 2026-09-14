from pydantic import BaseModel


class CategorySuggestionCreate(BaseModel):

    business_id: int

    suggested_category_id: int

    confidence: int

    reason: str | None = None



class CategorySuggestionResponse(BaseModel):

    id: int

    business_id: int

    suggested_category_id: int

    confidence: int

    reason: str | None = None

    status: str


    class Config:

        from_attributes = True