from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.sql import func

from app.database.database import Base



class ErrorOccurrence(Base):

    __tablename__ = "error_occurrences"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    error_code = Column(
        Integer,
        nullable=False,
        index=True
    )


    user_id = Column(
        Integer,
        nullable=True,
        index=True
    )


    action = Column(
        String,
        nullable=True
    )


    device_info = Column(
        JSON,
        nullable=True
    )


    context = Column(
        JSON,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )