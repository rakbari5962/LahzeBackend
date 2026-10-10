from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base


DATABASE_URL = "postgresql://postgres:5962@localhost:5432/lahze_company_restore"


engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
