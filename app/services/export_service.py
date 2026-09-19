import csv
import json
from uuid import uuid4
from pathlib import Path

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.core.paths import EXPORT_DIR
from app.schemas.chronostratigraphic_unit import ChronostratigraphicUnitRead


class ExportService:

    @staticmethod
    def export_units_to_csv(units: list[ChronostratigraphicUnitDB]) -> Path:

        fieldnames = [c.name for c in ChronostratigraphicUnitDB.__table__.columns]

        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

        csv_filename = f"exported_data_{uuid4().hex}.csv"
        csv_filepath = EXPORT_DIR.joinpath(csv_filename)

        with csv_filepath.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for unit in units:
                writer.writerow({
                    c.name: getattr(unit, c.name)
                    for c in ChronostratigraphicUnitDB.__table__.columns
                })

        return csv_filepath

    @staticmethod
    def export_units_to_json(units: list[ChronostratigraphicUnitDB]) -> Path:

        units_schema = [
            ChronostratigraphicUnitRead.model_validate(unit).model_dump(mode="json")
            for unit in units
        ]

        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

        json_filename = f"exported_data_{uuid4().hex}.json"
        json_filepath = EXPORT_DIR.joinpath(json_filename)

        with json_filepath.open("w") as json_file:
            json.dump(units_schema, json_file, indent=4, ensure_ascii=False)

        return json_filepath