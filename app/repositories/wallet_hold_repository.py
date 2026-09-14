from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.wallet_hold import WalletHold



def create_hold(
    db: Session,
    user_id: int,
    booking_id: int,
    amount: int
):

    hold = WalletHold(
        user_id=user_id,
        booking_id=booking_id,
        amount=amount,
        status="ACTIVE"
    )


    db.add(hold)
    db.commit()
    db.refresh(hold)


    return hold





def get_active_hold(
    db: Session,
    booking_id: int
):

    return db.query(WalletHold).filter(
        WalletHold.booking_id == booking_id,
        WalletHold.status == "ACTIVE"
    ).first()





def release_hold(
    db: Session,
    booking_id: int
):

    hold = get_active_hold(
        db,
        booking_id
    )


    if not hold:
        return None


    hold.status = "RELEASED"

    hold.released_at = datetime.now(
        timezone.utc
    )


    db.commit()
    db.refresh(hold)


    return hold





def capture_hold(
    db: Session,
    booking_id: int
):

    hold = get_active_hold(
        db,
        booking_id
    )


    if not hold:
        return None


    hold.status = "CAPTURED"


    db.commit()
    db.refresh(hold)


    return hold