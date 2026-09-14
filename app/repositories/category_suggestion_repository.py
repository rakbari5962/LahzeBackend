from sqlalchemy.orm import Session


from app.models.category_suggestion import CategorySuggestion

from app.models.business import Business





def create_category_suggestion(

    db: Session,

    business_id: int,

    suggested_category_id: int,

    confidence: int,

    reason: str | None = None,

    input_snapshot: dict | None = None

):


    suggestion = CategorySuggestion(

        business_id=business_id,

        suggested_category_id=suggested_category_id,

        confidence=confidence,

        reason=reason,

        status="PENDING",

        input_snapshot=input_snapshot

    )


    db.add(suggestion)

    db.commit()

    db.refresh(suggestion)


    return suggestion







def get_category_suggestion(

    db: Session,

    suggestion_id: int

):


    return db.query(CategorySuggestion).filter(

        CategorySuggestion.id == suggestion_id

    ).first()







def approve_category_suggestion(

    db: Session,

    suggestion: CategorySuggestion

):


    suggestion.status = "ACCEPTED"


    db.commit()

    db.refresh(suggestion)


    return suggestion







def reject_category_suggestion(

    db: Session,

    suggestion: CategorySuggestion

):


    suggestion.status = "REJECTED"


    db.commit()

    db.refresh(suggestion)


    return suggestion







def approve_category_suggestion_with_business_update(

    db: Session,

    suggestion: CategorySuggestion

):


    suggestion.status = "ACCEPTED"



    business = db.query(Business).filter(

        Business.id == suggestion.business_id

    ).first()



    if not business:

        raise Exception(

            "Business not found"

        )



    business.category_id = suggestion.suggested_category_id



    db.commit()


    db.refresh(suggestion)

    db.refresh(business)



    return suggestion