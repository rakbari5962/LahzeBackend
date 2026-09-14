from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base



class ErrorDefinition(Base):

    __tablename__ = "error_definitions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    error_code = Column(
        Integer,
        unique=True,
        nullable=False,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    description = Column(
        Text,
        nullable=False
    )


    severity = Column(
        String,
        default="MEDIUM"
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )