from pydantic import BaseModel



class TreasuryHealthResponse(BaseModel):

    treasury_balance: int

    total_commission_paid: int

    transaction_count: int