from pydantic import BaseModel, Field


class BusinessCategorySuggestionRequest(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None
    services: list[str] = Field(default_factory=list)


class PossibleCategoryMatchResponse(BaseModel):
    id: int
    name: str


class BusinessCategorySuggestionResponse(BaseModel):
    # Existing fields keep their meaning so older clients continue to work.
    category_id: int | None = None
    category_name: str | None = None
    confidence: int = Field(ge=0, le=100)
    reason: str
    # CATEGORY | ALIAS | KEYWORD | PROPOSAL | NONE
    match_type: str = "NONE"
    # Set only for PROPOSAL: a new, unapproved title. Nothing is persisted.
    proposed_title: str | None = None
    warning: str | None = None
    possible_matches: list[PossibleCategoryMatchResponse] = Field(default_factory=list)
