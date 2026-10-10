from fastapi import HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.category_proposal import (
    CategoryProposal,
    CategoryProposalBusiness,
    PROPOSAL_PENDING,
)
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate


def _has_pending_category_proposal(business_id):
    """EXISTS clause: the business is waiting for an admin category decision."""
    return (
        exists()
        .where(
            CategoryProposalBusiness.business_id == business_id,
            CategoryProposalBusiness.proposal_id == CategoryProposal.id,
            CategoryProposal.status == PROPOSAL_PENDING,
        )
    )


def create_opportunity(
    db: Session,
    opportunity: OpportunityCreate
):

    business = (
        db.query(Business)
        .filter(Business.id == opportunity.business_id)
        .with_for_update()
        .first()
    )

    if not business:
        raise HTTPException(status_code=404, detail="BUSINESS_NOT_FOUND")

    if business.is_deleted:
        raise HTTPException(status_code=409, detail="BUSINESS_DELETED")

    db_opportunity = Opportunity(

        business_id=opportunity.business_id,
        service_id=opportunity.service_id,

        start_time=opportunity.start_time,
        end_time=opportunity.end_time,

        original_price=opportunity.original_price,
        discount_percent=opportunity.discount_percent,
        final_price=opportunity.final_price,

        capacity=opportunity.capacity,
        reserved_count=0
    )


    db.add(db_opportunity)

    db.commit()

    db.refresh(db_opportunity)


    return db_opportunity



def get_opportunity(
    db: Session,
    opportunity_id: int
):

    return (
        db.query(Opportunity)
        .join(Business, Opportunity.business_id == Business.id)
        .filter(
            Opportunity.id == opportunity_id,
            Business.is_deleted == False,
            ~_has_pending_category_proposal(business_id=Opportunity.business_id),
        )
        .first()
    )



def get_active_opportunities(
    db: Session
):

    return (
        db.query(Opportunity)
        .join(Business, Opportunity.business_id == Business.id)
        .filter(
            Opportunity.status != "EXPIRED",
            Business.is_deleted == False,
            ~_has_pending_category_proposal(business_id=Opportunity.business_id),
        )
        .all()
    )



def get_business_opportunities(
    db: Session,
    business_id: int
):

    result = (
        db.query(Opportunity)
        .join(Business, Opportunity.business_id == Business.id)
        .filter(
            Opportunity.business_id == business_id,
            Opportunity.status != "EXPIRED",
            Business.is_deleted == False,
            ~_has_pending_category_proposal(business_id=Opportunity.business_id),
        )
        .all()
    )

    return result
