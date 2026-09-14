from pydantic import BaseModel



class MarketplaceOpportunityResponse(BaseModel):

    opportunity_id: int

    business_id: int

    business_name: str

    service_id: int

    service_name: str

    city_id: int

    start_time: str

    end_time: str

    original_price: int

    discount_percent: int

    final_price: int

    remaining_minutes: int