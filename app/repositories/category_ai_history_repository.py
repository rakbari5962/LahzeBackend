from sqlalchemy.orm import Session


from app.models.category_ai_history import CategoryAIHistory



def create_category_ai_history(
    db: Session,
    business_id: int,
    suggestion_id: int,
    suggested_category_id: int,
    action: str,
    confidence: int,
    input_snapshot: dict | None = None
):


    history = CategoryAIHistory(

        business_id=business_id,

        suggestion_id=suggestion_id,

        suggested_category_id=suggested_category_id,

        action=action,

        confidence=confidence,

        input_snapshot=input_snapshot

    )


    db.add(history)

    db.commit()

    db.refresh(history)


    return history





def get_category_ai_history(
    db: Session,
    business_id: int
):


    return (
        db.query(CategoryAIHistory)
        .filter(
            CategoryAIHistory.business_id == business_id
        )
        .order_by(
            CategoryAIHistory.created_at.desc()
        )
        .all()
    )