from app.core.security.admin_guard import admin_required

from app.schemas.admin_reward_schema import (
    PendingRewardsResponse,
    ProcessedRewardsResponse,
    FailedRewardsResponse,
    RewardStatisticsResponse
)

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.services.admin_reward_service import (
    get_pending_rewards_admin,
    get_processed_rewards_admin,
    get_reward_dashboard_stats,
    get_failed_rewards_admin
)





router = APIRouter(
    prefix="/admin/rewards",
    tags=["Admin Rewards"]
)





# --------------------------------------------------
# Database Dependency
# --------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()





# --------------------------------------------------
# Pending Rewards
# --------------------------------------------------

@router.get(
    "/pending",
    response_model=PendingRewardsResponse
)
def pending_rewards(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):

    return get_pending_rewards_admin(
        db
    )





# --------------------------------------------------
# Processed Rewards
# --------------------------------------------------

@router.get(
    "/released",
    response_model=ProcessedRewardsResponse
)
def released_rewards(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):

    return get_processed_rewards_admin(
        db
    )





# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

@router.get(
    "/stats",
    response_model=RewardStatisticsResponse
)
def reward_statistics(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):

    return get_reward_dashboard_stats(
        db
    )





# --------------------------------------------------
# Failed Releases
# --------------------------------------------------

@router.get(
    "/errors",
    response_model=FailedRewardsResponse
)
def reward_errors(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):

    return get_failed_rewards_admin(
        db
    )