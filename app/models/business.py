from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.sql import func

from app.database.database import Base





class Business(Base):

    __tablename__ = "businesses"



    id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )



    name = Column(
        String,
        nullable=False
    )



    category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=True,
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



    latitude = Column(
        Float,
        nullable=True
    )



    longitude = Column(
        Float,
        nullable=True
    )



    address = Column(
        String,
        nullable=True
    )



    description = Column(
        String,
        nullable=True
    )



    phone = Column(
        String,
        nullable=True
    )



    status = Column(
        String,
        default="ACTIVE"
    )



    # حذف نرم کسب و کار
    # False = قابل نمایش
    # True = حذف شده و نباید نمایش داده شود

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )



    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )



    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )