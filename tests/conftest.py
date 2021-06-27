import pytest
from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient
from foodie.config import DATABASE_URL
from foodie.db import models
from foodie.db.base import Base, get_engine, SessionLocal
from foodie.main import get_app
from foodie import util
from collections import namedtuple


AdminDetails = namedtuple(
    "AdminDetails", ["email", "password", "first_name", "last_name"]
)


@pytest.fixture(autouse=True)
def create_test_database():
    engine = get_engine(DATABASE_URL)
    metadata: MetaData = Base.metadata
    metadata.create_all(engine)
    yield  # Run the tests.
    metadata.drop_all(engine)


@pytest.fixture
def app() -> FastAPI:
    return get_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def admin_details():
    return AdminDetails("test@admin.com", "password", "Foodie", "Admin")


@pytest.fixture
def admin(session: Session, admin_details: AdminDetails) -> models.Admin:
    admin = models.Admin(
        email=admin_details.email,
        email_verified_on=datetime.utcnow(),
        hashed_password=util.hash_password(admin_details.password),
        first_name=admin_details.first_name,
        last_name=admin_details.last_name,
    )
    session.add(admin)
    session.commit()
    return admin
