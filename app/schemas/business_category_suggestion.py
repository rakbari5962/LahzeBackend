from pydantic import BaseModel


class BusinessCategorySuggestionRequest(BaseModel):

    name: str

    description: str | None = None

    services: list[str] = []



class BusinessCategorySuggestionResponse(BaseModel):

    category_id: int

    category_name: str

    confidence: int

    reason: str