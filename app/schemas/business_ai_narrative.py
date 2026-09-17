from pydantic import BaseModel

from typing import Optional



class BusinessAINarrativeResponse(BaseModel):

    business_id: int

    summary: str

    positive_summary: Optional[str] = None

    improvement_summary: Optional[str] = None

    trust_score: Optional[int] = None

    model_version: Optional[str] = None


    class Config:

        from_attributes = True