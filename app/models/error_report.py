from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base





class ErrorReport(Base):

    __tablename__ = "error_reports"



    id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    occurrence_id = Column(
        Integer,
        nullable=False
    )



    # توضیحی که سیستم به صورت خودکار تولید می‌کند
    # شامل شرح خطا، عملیات، context و اطلاعات فنی
    system_description = Column(
        Text,
        nullable=True
    )



    # توضیحی که کاربر هنگام گزارش اضافه می‌کند
    user_message = Column(
        Text,
        nullable=True
    )



    status = Column(
        String,
        default="OPEN"
    )



    admin_note = Column(
        Text,
        nullable=True
    )



    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )