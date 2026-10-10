"""Shared fixtures for category lifecycle tests.

Every test uses a private in-memory SQLite database and never touches the
application's configured database. The LLM client is always mocked.
"""

import pytest

from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (registers every table on Base.metadata)

from app.database.database import Base
from app.database.dependencies import get_db as app_get_db  # noqa: F401
from app.models.business import Business
from app.models.business_category import BusinessCategory
from app.models.category_alias import BusinessCategoryAlias
from app.models.category_proposal import (  # noqa: F401
    CategoryProposal,
    CategoryProposalBusiness,
    CategoryProposalHistory,
)
from app.models.session import Session as LoginSession
from app.models.user import User


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # pysqlite does not emit BEGIN itself, which breaks SAVEPOINT/ROLLBACK
    # semantics. Standard SQLAlchemy workaround so rollback tests are truthful.
    @event.listens_for(engine, "connect")
    def _no_implicit_begin(dbapi_connection, _record):
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, "begin")
    def _emit_begin(conn):
        conn.exec_driver_sql("BEGIN")

    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False, autocommit=False)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def categories(db):
    health = BusinessCategory(name="سلامت و درمان", slug="health", is_active=True)
    beauty = BusinessCategory(name="زیبایی و مراقبت شخصی", slug="beauty", is_active=True)
    restaurant = BusinessCategory(name="رستوران و کافه", slug="restaurant", is_active=True)
    inactive = BusinessCategory(name="دسته غیرفعال", slug="inactive-one", is_active=False)

    db.add_all([health, beauty, restaurant, inactive])
    db.flush()

    db.add(
        BusinessCategoryAlias(
            category_id=health.id,
            alias="Psychologist",
            normalized_alias="psychologist",
        )
    )
    db.flush()

    return {
        "health": health,
        "beauty": beauty,
        "restaurant": restaurant,
        "inactive": inactive,
    }


@pytest.fixture()
def owner(db):
    user = User(phone_number="09120000001", role="CUSTOMER", profile_completed=True)
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def admin(db):
    user = User(phone_number="09120000002", role="ADMIN", profile_completed=True)
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def admin_session(db, admin):
    session = LoginSession(
        user_id=admin.id,
        token="admin-session-token",
        is_active=True,
        is_temporary=False,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    db.add(session)
    db.flush()
    return session


@pytest.fixture()
def customer_session(db, owner):
    session = LoginSession(
        user_id=owner.id,
        token="customer-session-token",
        is_active=True,
        is_temporary=False,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    db.add(session)
    db.flush()
    return session


@pytest.fixture()
def other_business(db, owner):
    item = Business(name="کسب‌وکار دیگر", owner_user_id=owner.id, province_id=1, city_id=1)
    db.add(item)
    db.flush()
    return item