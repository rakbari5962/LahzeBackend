from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base





class OTPRequest(Base):

    __tablename__ = "otp_requests"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    phone_number = Column(

        String,

        nullable=False,

        index=True

    )


    code = Column(

        String,

        nullable=False

    )


    expires_at = Column(

        DateTime(timezone=True),

        nullable=False

    )


    is_verified = Column(

        Boolean,

        default=False

    )


    verified_at = Column(

        DateTime(timezone=True),

        nullable=True

    )


    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )