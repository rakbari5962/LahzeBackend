from sqlalchemy.orm import Session

from app.models.review_attribute import ReviewAttribute
from app.models.business_attribute_score import BusinessAttributeScore



def get_attribute_by_key(
    db: Session,
    key: str
):

    return db.query(
        ReviewAttribute
    ).filter(
        ReviewAttribute.key == key
    ).first()





def create_attribute(
    db: Session,
    key: str,
    label: str,
    category: str = None
):

    attribute = ReviewAttribute(

        key=key,

        label=label,

        category=category

    )


    db.add(attribute)

    db.commit()

    db.refresh(attribute)


    return attribute





def get_or_create_attribute(
    db: Session,
    key: str,
    label: str,
    category: str = None
):

    attribute = get_attribute_by_key(
        db=db,
        key=key
    )


    if attribute:

        return attribute


    return create_attribute(
        db=db,
        key=key,
        label=label,
        category=category
    )





def get_business_attribute_score(
    db: Session,
    business_id: int,
    attribute_id: int
):

    return db.query(
        BusinessAttributeScore
    ).filter(
        BusinessAttributeScore.business_id == business_id,
        BusinessAttributeScore.attribute_id == attribute_id
    ).first()





def create_business_attribute_score(
    db: Session,
    business_id: int,
    attribute_id: int
):

    score = BusinessAttributeScore(

        business_id=business_id,

        attribute_id=attribute_id,

        positive_count=0,

        negative_count=0

    )


    db.add(score)

    db.commit()

    db.refresh(score)


    return score





def get_or_create_business_attribute_score(
    db: Session,
    business_id: int,
    attribute_id: int
):

    score = get_business_attribute_score(
        db=db,
        business_id=business_id,
        attribute_id=attribute_id
    )


    if score:

        return score


    return create_business_attribute_score(
        db=db,
        business_id=business_id,
        attribute_id=attribute_id
    )





def increase_positive_count(
    db: Session,
    score: BusinessAttributeScore
):

    score.positive_count += 1

    db.commit()

    db.refresh(score)


    return score





def increase_negative_count(
    db: Session,
    score: BusinessAttributeScore
):

    score.negative_count += 1

    db.commit()

    db.refresh(score)


    return score