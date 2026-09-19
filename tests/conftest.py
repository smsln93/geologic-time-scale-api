import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database.session import get_db
from app.main import app
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB

from sqlalchemy import create_engine, StaticPool

from app.database.base import Base
from tests.settings import TestSettings


test_engine = create_engine(TestSettings.TEST_DATABASE_URL,
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind=test_engine,
                                   autoflush=False,
                                   autocommit=False)

@pytest.fixture(scope="function", autouse=True)
def override_dependencies():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

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


@pytest.fixture(autouse=True)
def env_setup():
    os.environ["API_KEY"] = TestSettings.TEST_API_KEY
    os.environ["DATABASE_URL"] = TestSettings.TEST_DATABASE_URL


@pytest.fixture
def valid_authentication_header():
    return {"X-API-Key": TestSettings.TEST_API_KEY}


@pytest.fixture
def invalid_authentication_header():
    return {"X-API-Key": "invalid-api-key"}


@pytest.fixture
def auth_client(client):
    client.headers.update({"X-API-Key": TestSettings.TEST_API_KEY})
    return client


@pytest.fixture
def test_db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def pleistocene_unit(test_db_session):

    db = TestingSessionLocal()

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

    db.add(pleistocene)
    db.commit()
    return pleistocene


@pytest.fixture
def mesozoic_unit(test_db_session):

    db = TestingSessionLocal()

    mesozoic = ChronostratigraphicUnitDB(
        id="mesozoic",
        name="Mesozoic",
        rank="Era",
        rank_order=3,
        begin_time_ma=251.902,
        begin_uncertainty_ma=0.024,
        end_time_ma=66.0,
        end_uncertainty_ma=0.0,
        parent_id=None
    )

    triassic = ChronostratigraphicUnitDB(
        id="triassic",
        name="Triassic",
        rank="Period",
        rank_order=4,
        begin_time_ma=251.902,
        begin_uncertainty_ma=0.024,
        end_time_ma=201.4,
        end_uncertainty_ma=0.2,
        parent_id="mesozoic")

    jurassic = ChronostratigraphicUnitDB(
        id="jurassic",
        name="Jurassic",
        rank="Period",
        rank_order=4,
        begin_time_ma=201.4,
        begin_uncertainty_ma=0.2,
        end_time_ma=143.1,
        end_uncertainty_ma=0.6,
        parent_id="mesozoic")

    early_jurassic = ChronostratigraphicUnitDB(
        id="early-jurassic",
        name="Early Jurassic",
        rank="Epoch",
        rank_order=5,
        begin_time_ma=201.4,
        begin_uncertainty_ma=0.2,
        end_time_ma=174.7,
        end_uncertainty_ma=0.8,
        parent_id="jurassic"
    )

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

    aalenian = ChronostratigraphicUnitDB(
        id="aalenian",
        name="Aalenian",
        rank="Age",
        rank_order=6,
        begin_time_ma=174.7,
        begin_uncertainty_ma=0.8,
        end_time_ma=170.9,
        end_uncertainty_ma=0.8,
        parent_id="middle-jurassic"
    )

    bajocian = ChronostratigraphicUnitDB(
        id="bajocian",
        name="Bajocian",
        rank="Age",
        rank_order=6,
        begin_time_ma=170.9,
        begin_uncertainty_ma=0.8,
        end_time_ma=168.2,
        end_uncertainty_ma=1.2,
        parent_id="middle-jurassic"
    )

    bathonian = ChronostratigraphicUnitDB(
        id="bathonian",
        name="Bathonian",
        rank="Age",
        rank_order=6,
        begin_time_ma=168.2,
        begin_uncertainty_ma=1.2,
        end_time_ma=165.3,
        end_uncertainty_ma=1.1,
        parent_id="middle-jurassic"
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

    late_jurassic = ChronostratigraphicUnitDB(
        id="late-jurassic",
        name="Late Jurassic",
        rank="Epoch",
        rank_order=5,
        begin_time_ma=161.5,
        begin_uncertainty_ma=1.0,
        end_time_ma=143.1,
        end_uncertainty_ma=0.6,
        parent_id="jurassic"
    )

    cretaceous = ChronostratigraphicUnitDB(
        id="cretaceous",
        name="Cretaceous",
        rank="Period",
        rank_order=4,
        begin_time_ma=143.1,
        begin_uncertainty_ma=0.6,
        end_time_ma=66.0,
        end_uncertainty_ma=0.0,
        parent_id="mesozoic"
    )

    db.add_all([mesozoic,
                triassic,
                jurassic,
                early_jurassic,
                middle_jurassic,
                aalenian,
                bajocian,
                bathonian,
                callovian,
                late_jurassic,
                cretaceous])
    db.commit()
    return mesozoic
