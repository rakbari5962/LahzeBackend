from fastapi import Depends, HTTPException, status


from app.core.security.auth import get_current_user


from app.models.user import User





def require_admin(

    current_user: User = Depends(
        get_current_user
    )

):


    if current_user.role != "ADMIN":

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail={

                "error":
                    "ADMIN_PERMISSION_REQUIRED"

            }

        )



    return current_user