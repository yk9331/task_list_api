import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core.config import settings
from tests.utils.dummy_data_generator import create_dummy_data


@pytest.fixture(scope="session")
def app():
    from src.main import app

    yield app


@pytest.fixture(scope="session")
def db():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        **settings.SQLALCHEMY_ENGINE_OPTIONS,
    )

    connection = engine.connect()
    session = Session(bind=connection)
    create_dummy_data(session)

    yield engine


@pytest.fixture(scope="class", autouse=True)
def session(app, db):
    """
    Returns an sqlalchemy session, and after the test tears down everything properly.
    """
    from src.core.db.session import get_db

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
    if transaction.is_active:
        transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_client(app):
    """
    Overrides the auth_user dependency to bypass authentication.
    Should return valid test user after user services are implemented.
    """
    from src.core.auth import auth_user

    with TestClient(app) as c:
        app.dependency_overrides[auth_user] = lambda: None
        yield c
        app.dependency_overrides = {}
