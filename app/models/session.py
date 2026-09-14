from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base





class Session(Base):

    __tablename__ = "sessions"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    user_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=False,

        index=True

    )


    token = Column(

        String,

        unique=True,

        nullable=False,

        index=True

    )


    is_active = Column(

        Boolean,

        default=True

    )


    is_temporary = Column(

        Boolean,

        default=False,

        nullable=False

    )


    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )


    expires_at = Column(

        DateTime(timezone=True),

        nullable=False

    )