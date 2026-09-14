from sqlalchemy.orm import Session

from app.models.business_category import BusinessCategory



def get_categories(
    db: Session
):

    return db.query(BusinessCategory).filter(

        BusinessCategory.is_active == True

    ).all()





def get_category(
    db: Session,
    category_id: int
):

    return db.query(BusinessCategory).filter(

        BusinessCategory.id == category_id

    ).first()