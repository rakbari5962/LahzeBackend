from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):

    total_commission_paid: int

    total_releases: int

    pending_commissions: int

    failed_commissions: int

    active_referrers: int

    earning_referrers: int