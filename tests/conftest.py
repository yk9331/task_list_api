import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import settings
from src.db.base import Base


@pytest.fixture(scope="session")
def app():
    from src.main import fastapi_app

    yield fastapi_app


@pytest.fixture(scope="session")
def db():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        **settings.SQLALCHEMY_ENGINE_OPTIONS,
    )

    connection = engine.connect()
    session = Session(bind=connection)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture(scope="class", autouse=True)
def session(app, db):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    from src.db.session import get_db

    connection = db.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    # override app dependencies
    app.dependency_overrides[get_db] = lambda: session

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c
