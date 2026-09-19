from pydantic import BaseModel

from typing import List, Dict, Any, Optional



class ReviewAIAnalysisResponse(BaseModel):

    business_id: int

    total_reviews: int

    average_rating: Optional[str] = None


    strengths: List[Dict[str, Any]]

    weaknesses: List[Dict[str, Any]]

    themes: List[Dict[str, Any]]

    customer_sentiment: Dict[str, Any]

    attribute_summary: Optional[Dict[str, Any]] = None

    model_version: Optional[str] = None



    class Config:

        from_attributes = True