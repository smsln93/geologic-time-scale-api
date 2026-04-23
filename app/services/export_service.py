import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.core.paths import EXPORT_DIR
from app.schemas.chronostratigraphic_unit import ChronostratigraphicUnitRead


class ExportService:

    @staticmethod
    def export_units_to_csv(units: List[ChronostratigraphicUnitDB]) -> Path:

        fieldnames = [c.name for c in ChronostratigraphicUnitDB.__table__.columns]

        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

        csv_filename = f"exported_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_filepath = EXPORT_DIR.joinpath(csv_filename)

        with csv_filepath.open("w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for unit in units:
                writer.writerow({
                    c.name: getattr(unit, c.name)
                    for c in ChronostratigraphicUnitDB.__table__.columns
                })

        return csv_filepath

    @staticmethod
    def export_units_to_json(units: List[ChronostratigraphicUnitDB]) -> Path:

        units_schema = [
            ChronostratigraphicUnitRead.model_validate(unit).model_dump(mode="json")
            for unit in units
        ]

        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

        json_filename = f"exported_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        json_filepath = EXPORT_DIR.joinpath(json_filename)

        with json_filepath.open("w") as json_file:
            json.dump(units_schema, json_file, indent=4)

        return json_filepath