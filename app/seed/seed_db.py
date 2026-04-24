import json
from pathlib import Path

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.database.base import Base
from app.database.session import create_session_local


def seed_db(session):
    base_path = Path(__file__).parent.joinpath("input")
    files = base_path.glob("*.json")
    '''
    files = ["precambrian.json",
             "hadean.json",
             "archean.json",
             "proterozoic.json",
             "phanerozoic.json",
             "paleozoic.json",
             "mesozoic.json",
             "cenozoic.json"]

    '''

    for file in files:
        with base_path.joinpath(file).open(mode="r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        session.add(ChronostratigraphicUnitDB(**item) for item in data)
        session.commit()


def run_seed(seed_engine):
    Base.metadata.drop_all(seed_engine)
    Base.metadata.create_all(seed_engine)

    SessionLocal = create_session_local()
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()


if __name__ == '__main__':
    from app.database.engine import get_database_engine
    engine = get_database_engine()
    run_seed(engine)



