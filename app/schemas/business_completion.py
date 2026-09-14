from pydantic import BaseModel



class BusinessCompletionResponse(BaseModel):

    business_id: int

    completion_percentage: int

    is_complete: bool

    missing_items: list[str]

    completed_items: list[str]