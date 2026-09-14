from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.database import Base





class UserDevice(Base):

    __tablename__ = "user_devices"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    user_id = Column(

        Integer,

        ForeignKey(
            "users.id"
        ),

        nullable=False,

        index=True

    )



    device_id = Column(

        String,

        unique=True,

        nullable=False,

        index=True

    )



    platform = Column(

        String,

        nullable=False

    )



    device_model = Column(

        String,

        nullable=True

    )



    os_version = Column(

        String,

        nullable=True

    )



    app_version = Column(

        String,

        nullable=True

    )



    push_token = Column(

        Text,

        nullable=True

    )



    is_active = Column(

        Boolean,

        default=True

    )



    last_seen_at = Column(

        DateTime(timezone=True),

        nullable=True

    )



    user = relationship(

        "User",

        back_populates="devices"

    )



    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )



    updated_at = Column(

        DateTime(timezone=True),

        onupdate=func.now()

    )