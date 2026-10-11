from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean
)

from app.database.database import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
)

from sqlalchemy.orm import relationship

from app.database.database import Base



class City(Base):

    __tablename__ = "cities"



    id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    name = Column(
        String,
        nullable=False
    )



    province_id = Column(
        Integer,
        ForeignKey("provinces.id"),
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )


    # وضعیت فعال بودن شهر
    # True = شهر فعال و قابل استفاده در Lahze
    # False = شهر غیرفعال

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )



    province = relationship(
        "Province",
        back_populates="cities"
    )