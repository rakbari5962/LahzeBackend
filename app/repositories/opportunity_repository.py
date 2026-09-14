from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate


def create_opportunity(
    db: Session,
    opportunity: OpportunityCreate
):
    db_opportunity = Opportunity(
        business_id=opportunity.business_id,
        service_id=opportunity.service_id,

        start_time=opportunity.start_time,
        end_time=opportunity.end_time,

        original_price=opportunity.original_price,
        discount_percent=opportunity.discount_percent,
        final_price=opportunity.final_price,

        capacity=opportunity.capacity
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
        .filter(
            Opportunity.id == opportunity_id
        )
        .first()
    )


def get_active_opportunities(
    db: Session
):
    return (
        db.query(Opportunity)
        .filter(
            Opportunity.status == "ACTIVE",
            Opportunity.capacity > 0
        )
        .all()
    )