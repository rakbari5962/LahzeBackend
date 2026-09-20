from pydantic import BaseModel
from typing import Optional, Dict, Any, List



class BusinessPublicInfo(BaseModel):

    id: int

    name: str

    description: Optional[str] = None

    phone: Optional[str] = None






class CustomerExperienceItem(BaseModel):

    title: str

    total_mentions: int

    positive_mentions: int

    negative_mentions: int

    positive_percentage: float

    negative_percentage: float

    confidence: str






class CustomerExperience(BaseModel):

    title: str

    items: List[CustomerExperienceItem]






class ReputationSummary(BaseModel):

    business_id: int

    total_reviews: int

    average_rating: Optional[str] = None

    customer_sentiment: Dict[str, Any]

    model_version: Optional[str] = None






class PublicBusinessProfileResponse(BaseModel):

    business: BusinessPublicInfo

    reputation: ReputationSummary

    customer_experience: CustomerExperience