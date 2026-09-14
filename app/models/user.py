from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.database import Base





class User(Base):

    __tablename__ = "users"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    phone_number = Column(

        String,

        unique=True,

        nullable=False,

        index=True

    )


    province_id = Column(

        Integer,

        ForeignKey("provinces.id"),

        nullable=True

    )


    city_id = Column(

        Integer,

        ForeignKey("cities.id"),

        nullable=True

    )


    role = Column(

        String,

        nullable=False,

        default="CUSTOMER"

    )


    profile_completed = Column(

        Boolean,

        nullable=False,

        default=False

    )


    devices = relationship(

        "UserDevice",

        back_populates="user",

        cascade="all, delete-orphan"

    )


    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )


    updated_at = Column(

        DateTime(timezone=True),

        onupdate=func.now()

    )