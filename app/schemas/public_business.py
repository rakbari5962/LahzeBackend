from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Literal



class BusinessPublicInfo(BaseModel):

    id: int

    name: str

    description: Optional[str] = None

    phone: Optional[str] = None



class CustomerInsightItem(BaseModel):

    label: str

    mentions: int

    score: float

    confidence: Literal[
        "low",
        "medium",
        "high"
    ]



class CustomerInsights(BaseModel):

    strengths: List[CustomerInsightItem]

    weaknesses: List[CustomerInsightItem]



class ReputationSummary(BaseModel):

    business_id: int

    total_reviews: int

    average_rating: Optional[str] = None

    customer_sentiment: Dict[str, Any]

    model_version: Optional[str] = None



class PublicBusinessProfileResponse(BaseModel):

    business: BusinessPublicInfo

    reputation: ReputationSummary

    customer_insights: CustomerInsights