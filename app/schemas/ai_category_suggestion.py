from pydantic import BaseModel


class CategorySuggestionRequest(BaseModel):

    business_name: str

    services: list[str]

    description: str | None = None