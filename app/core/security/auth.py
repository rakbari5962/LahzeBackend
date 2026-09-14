from fastapi import Depends, Header, HTTPException, status

from sqlalchemy.orm import Session


from app.database.dependencies import get_db

from app.models.user import User





def get_current_user(

    x_user_id: int = Header(
        None,
        alias="X-User-ID"
    ),

    db: Session = Depends(get_db)

):


    if not x_user_id:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail={
                "error": "USER_ID_REQUIRED"
            }

        )



    user = db.query(

        User

    ).filter(

        User.id == x_user_id

    ).first()



    if not user:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail={

                "error": "USER_NOT_FOUND"

            }

        )



    return user