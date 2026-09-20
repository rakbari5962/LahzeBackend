from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Literal



class BusinessPublicInfo(BaseModel):

    id: int

    name: str

    description: Optional[str] = None

    phone: Optional[str] = None





class CustomerExperienceItem(BaseModel):

    title: str

    status: Literal[
        "strength",
        "improvement"
    ]

    percentage: float

    mentions: int

    color: Literal[
        "green",
        "red"
    ]





class CustomerExperience(BaseModel):

    title: str

    strengths: List[CustomerExperienceItem]

    improvements: List[CustomerExperienceItem]





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