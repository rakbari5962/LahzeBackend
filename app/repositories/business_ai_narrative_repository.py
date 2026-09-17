from sqlalchemy.orm import Session

from app.models.business_ai_narrative import BusinessAINarrative



def get_business_narrative(
    db: Session,
    business_id: int
):

    return db.query(
        BusinessAINarrative
    ).filter(
        BusinessAINarrative.business_id == business_id
    ).first()





def create_or_update_narrative(
    db: Session,
    business_id: int,
    data: dict
):

    narrative = get_business_narrative(
        db,
        business_id
    )


    if narrative:

        narrative.summary = data["summary"]

        narrative.positive_summary = data["positive_summary"]

        narrative.improvement_summary = data["improvement_summary"]

        narrative.trust_score = data["trust_score"]

        narrative.model_version = data["model_version"]



    else:

        narrative = BusinessAINarrative(

            business_id=business_id,

            summary=data["summary"],

            positive_summary=data["positive_summary"],

            improvement_summary=data["improvement_summary"],

            trust_score=data["trust_score"],

            model_version=data["model_version"]

        )


        db.add(narrative)



    db.commit()

    db.refresh(narrative)


    return narrative