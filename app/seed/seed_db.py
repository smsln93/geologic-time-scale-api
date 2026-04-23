import json
from pathlib import Path

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.database.base import Base
from app.database.engine import engine
from app.database.session import create_session_local


def seed_db(session):
    base_path = Path(__file__).parent.joinpath("input")

    files = ["precambrian.json",
             "hadean.json",
             "archean.json",
             "proterozoic.json",
             "phanerozoic.json",
             "paleozoic.json",
             "mesozoic.json",
             "cenozoic.json"]

    try:
        for file in files:
            with open(base_path.joinpath(file), "r") as json_file:
                data = json.load(json_file)

            for item in data:
                session.add(ChronostratigraphicUnitDB(**item))

        session.commit()
    except Exception as e:
        session.rollback()
        raise


def run_seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionLocal = create_session_local(engine)
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()


if __name__ == '__main__':
    run_seed()



