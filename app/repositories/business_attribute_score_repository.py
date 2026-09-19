from sqlalchemy.orm import Session

from app.models.business_attribute_score import BusinessAttributeScore
from app.models.review_attribute import ReviewAttribute



def get_business_attribute_scores(
    db: Session,
    business_id: int
):

    return (
        db.query(
            BusinessAttributeScore,
            ReviewAttribute
        )
        .join(
            ReviewAttribute,
            ReviewAttribute.id ==
            BusinessAttributeScore.attribute_id
        )
        .filter(
            BusinessAttributeScore.business_id == business_id
        )
        .all()
    )