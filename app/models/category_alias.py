from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.database import Base


class BusinessCategoryAlias(Base):

    __tablename__ = "business_category_aliases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("business_categories.id"),
        nullable=False,
        index=True
    )

    alias = Column(
        String,
        nullable=False
    )

    # One normalized alias maps to exactly one category.
    normalized_alias = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
