import argparse
import json
from pathlib import Path
from typing import Optional

from app.database.base import Base
from app.database.session import create_session_local
from app.database.engine import get_database_engine
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB


INPUT_DATA = Path(__file__).resolve().parent.joinpath("input")


def load_units():
    units = []

    for file in INPUT_DATA.glob("*.json"):
        with file.open(mode="r", encoding="utf-8") as f:
            data_json = json.load(f)

        units.extend(ChronostratigraphicUnitDB(**item)
                     for item in data_json)

    return units


def run_db_seed(db_url: Optional[str] = None):
    engine = get_database_engine(db_url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    SessionLocal = create_session_local(db_url=db_url)
    session = SessionLocal()

    try:
        session.add_all(load_units())
        session.commit()
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="Create or reset database")
    parser.add_argument("--db-url", type=str, required=False, help="Optional database URL override")

    args = parser.parse_args()

    run_db_seed(args.db_url)


if __name__ == "__main__":
    main()