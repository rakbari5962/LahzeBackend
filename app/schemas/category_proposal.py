from datetime import datetime

from pydantic import BaseModel, Field


class CategoryProposalApproveRequest(BaseModel):
    note: str | None = Field(default=None, max_length=500)


class CategoryProposalRejectRequest(BaseModel):
    # Required: rejection always supplies the title that becomes the category.
    replacement_title: str = Field(min_length=2, max_length=60)
    note: str | None = Field(default=None, max_length=500)


class CategoryProposalBusinessResponse(BaseModel):
    id: int
    name: str
    category_id: int | None = None

    class Config:
        from_attributes = True


class CategoryProposalHistoryResponse(BaseModel):
    id: int
    proposal_id: int
    original_title: str
    from_status: str
    to_status: str
    decision: str
    admin_user_id: int | None = None
    replacement_title: str | None = None
    final_category_id: int | None = None
    note: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class PossibleCategoryMatch(BaseModel):
    id: int
    name: str


class CategoryProposalResponse(BaseModel):
    id: int
    title: str
    source: str
    status: str
    final_category_id: int | None = None
    reviewed_by_user_id: int | None = None
    review_note: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class CategoryProposalDetailResponse(CategoryProposalResponse):
    businesses: list[CategoryProposalBusinessResponse] = []
    history: list[CategoryProposalHistoryResponse] = []
    possible_matches: list[PossibleCategoryMatch] = []


class CategoryProposalPage(BaseModel):
    items: list[CategoryProposalResponse]
    page: int
    page_size: int
    total: int
