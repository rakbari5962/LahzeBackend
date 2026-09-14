from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base



class BusinessCategory(Base):

    __tablename__ = "business_categories"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    name = Column(

        String,

        nullable=False

    )


    slug = Column(

        String,

        unique=True,

        nullable=False,

        index=True

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