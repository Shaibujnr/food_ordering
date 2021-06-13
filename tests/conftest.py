import pytest
from fastapi import FastAPI
from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient
from foodie.db.base import Base, engine, SessionLocal
from foodie.main import get_app


@pytest.fixture(autouse=True)
def create_test_database():
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
