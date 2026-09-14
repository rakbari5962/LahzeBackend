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



class BusinessService(Base):

    __tablename__ = "business_services"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    business_id = Column(

        Integer,

        ForeignKey("businesses.id"),

        nullable=False,

        index=True

    )


    name = Column(

        String,

        nullable=False

    )


    category = Column(

        String,

        nullable=True

    )


    duration_minutes = Column(

        Integer,

        nullable=True

    )


    price = Column(

        Integer,

        nullable=True

    )


    description = Column(

        String,

        nullable=True

    )


    is_active = Column(

        Boolean,

        nullable=False,

        default=True

    )


    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )


    updated_at = Column(

        DateTime(timezone=True),

        onupdate=func.now()

    )