import pytest
from fastapi.testclient import TestClient

from app.database.session import create_session_local, get_db
from app.core.security import verify_api_key
from app.main import app
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB

from sqlalchemy import create_engine, StaticPool

from app.database.base import Base
from tests.settings import TestSettings


test_engine = create_engine(TestSettings.TEST_DATABASE_URL,
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool)

TestingSessionLocal = create_session_local(test_engine)


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = get_db(TestingSessionLocal)
    app.dependency_overrides[verify_api_key] = lambda: TestSettings.TEST_API_KEY

    yield

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)


@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
        db.rollback()
    finally:
        db.close()


@pytest.fixture
def valid_authentication_header():
    return {"X-API-Key": TestSettings.TEST_API_KEY}


@pytest.fixture
def invalid_authentication_header():
    return {"X-API-Key": "invalid-api-key"}


@pytest.fixture
def pleistocene_unit(session):
    pleistocene = ChronostratigraphicUnitDB(
        id="pleistocene",
        name="Pleistocene",
        rank="Epoch",
        rank_order=5,
        begin_time_ma=2.58,
        begin_uncertainty_ma=0.0,
        end_time_ma=0.0117,
        end_uncertainty_ma=0.0,
        parent_id=None,
    )

    session.add(pleistocene)
    session.commit()
    return pleistocene


@pytest.fixture
def mesozoic_unit(session):

    mesozoic = ChronostratigraphicUnitDB(
        id="mesozoic",
        name="Mesozoic",
        rank="Era",
        rank_order=2,
        begin_time_ma=250.0,
        begin_uncertainty_ma=1.5,
        end_time_ma=66.0,
        end_uncertainty_ma=0.6,
        parent_id=None
    )

    jurassic = ChronostratigraphicUnitDB(
        id="jurassic",
        name="Jurassic",
        rank="Period",
        rank_order=2,
        begin_time_ma=200.0,
        begin_uncertainty_ma=1.5,
        end_time_ma=140.0,
        end_uncertainty_ma=0.6,
        parent_id="mesozoic")

    middle_jurassic = ChronostratigraphicUnitDB(
        id="middle-jurassic",
        name="Middle Jurassic",
        rank="Epoch",
        rank_order=5,
        begin_time_ma=174.7,
        begin_uncertainty_ma=0.8,
        end_time_ma=161.5,
        end_uncertainty_ma=1.0,
        parent_id="jurassic"
    )

    callovian = ChronostratigraphicUnitDB(
        id="callovian",
        name="Callovian",
        rank="Age",
        rank_order=6,
        begin_time_ma=165.3,
        begin_uncertainty_ma=1.1,
        end_time_ma=161.5,
        end_uncertainty_ma=1.0,
        parent_id="middle-jurassic"
    )

    session.add_all([mesozoic, jurassic, middle_jurassic, callovian])
    session.commit()
    return mesozoic
