from sqlalchemy.orm import Session


from app.repositories.business_ai_narrative_repository import (
    get_business_narrative
)



def get_business_ai_summary(
    db: Session,
    business_id: int
):

    narrative = get_business_narrative(
        db,
        business_id
    )


    if not narrative:

        return None



    return narrative