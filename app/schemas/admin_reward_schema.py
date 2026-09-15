from pydantic import BaseModel

from typing import List, Optional

from datetime import datetime





# --------------------------------------------------
# Reward Item
# --------------------------------------------------

class RewardEventResponse(BaseModel):

    reward_event_id: int

    user_id: int

    booking_id: int

    amount: int

    type: str

    status: str

    transaction_id: Optional[str] = None

    created_at: Optional[datetime] = None





# --------------------------------------------------
# Pending Rewards Response
# --------------------------------------------------

class PendingRewardsResponse(BaseModel):

    count: int

    items: List[RewardEventResponse]





# --------------------------------------------------
# Processed Rewards Response
# --------------------------------------------------

class ProcessedRewardsResponse(BaseModel):

    count: int

    total_amount: int

    items: List[RewardEventResponse]





# --------------------------------------------------
# Failed Transaction
# --------------------------------------------------

class FailedRewardResponse(BaseModel):

    transaction_id: str

    type: str

    status: str

    amount: int

    reference_type: str

    reference_id: int

    created_at: Optional[datetime] = None





class FailedRewardsResponse(BaseModel):

    count: int

    items: List[FailedRewardResponse]





# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

class RewardStatisticsResponse(BaseModel):

    pending_count: int

    pending_amount: int

    processed_count: int

    processed_amount: int

    failed_count: int