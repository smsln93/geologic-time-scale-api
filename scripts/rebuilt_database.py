import argparse
import json
from pathlib import Path

from app.database.base import Base
from app.database.session import create_session_local
from app.database.engine import get_database_engine
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB


INPUT_DATA = Path(__file__).resolve().parent.joinpath("input")


def load_units(units_dir: Path = INPUT_DATA, selected_units_names: list[str] = None):
    units: list[ChronostratigraphicUnitDB] = []

    if selected_units_names is None:
        selected_units_paths = list(units_dir.glob("*.json"))
    else:
        selected_units_paths = [units_dir.joinpath(f"{name}.json") for name in selected_units_names]

    for file in selected_units_paths:
        try:
            with file.open(mode="r", encoding="utf-8") as f:
                data_json = json.load(f)
        except FileNotFoundError as fnf:
            raise FileNotFoundError(f"Missing unit file: {file}") from fnf
        except json.JSONDecodeError as jsn:
            raise ValueError(f"Invalid JSON file: {file}") from jsn

        units.extend(ChronostratigraphicUnitDB(**item)
                     for item in data_json)

    return units


def run_db_seed(units: list[ChronostratigraphicUnitDB], db_url: str | None):
    engine = get_database_engine(db_url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    SessionLocal = create_session_local(db_url=db_url)
    session = SessionLocal()

    try:
        pending = {unit.id: unit for unit in units}
        inserted = set()

        while pending:
            ready = [unit for unit in pending.values()
                     if unit.parent_id is None or unit.parent_id in inserted]

            if not ready:
                raise ValueError("Cannot resolve unit hierarchy: cycle or missing parent")

            session.add_all(ready)
            session.flush()

            for unit in ready:
                inserted.add(unit.id)
                del pending[unit.id]

        session.commit()
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="Create or reset database")
    parser.add_argument("--db-path", type=Path, required=True, help="Path to SQLite database")
    parser.add_argument("--data-dir", type=Path, default=INPUT_DATA, help="Path to the directory with unit data")
    parser.add_argument("--units", nargs='+', required=False, help="Optional list of unit names to be included")

    args = parser.parse_args()

    units = load_units(units_dir=args.data_dir,
                       selected_units_names=args.units)

    if not units:
        parser.error("No units specified to build database")

    db_path = f"sqlite:///{args.db_path.resolve().as_posix()}"

    run_db_seed(units, db_path)


if __name__ == "__main__":
    main()