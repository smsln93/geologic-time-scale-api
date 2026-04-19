import csv
import json
from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config.config_paths import EXPORT_DIR
from app.database.session import get_db
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.schemas.chronostratigraphic_unit import ChronostratigraphicUnitBase
from app.api.router import api_router


@api_router.get(path="/export/csv",
                tags=["Export"],
                summary="Export units to CSV",
                description="Exports all geologic units as a downloadable CSV file")
def export_units_csv(db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()
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

    return FileResponse(
        path=csv_filepath,
        media_type="text/csv",
        filename=csv_filename
    )


@api_router.get(path="/export/json",
                tags=["Export"],
                summary="Export units to JSON",
                description="Exports all geologic units as a downloadable JSON file")
def export_units_json(db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()
    if not units:
        raise HTTPException(status_code=404, detail="No seed to export")

    units_schema = [
        ChronostratigraphicUnitBase.model_validate(unit).to_json_dict()
        for unit in units
    ]

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_filename = f"exported_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_filepath = EXPORT_DIR.joinpath(json_filename)

    with open(json_filepath, "w") as json_file:
        json.dump(units_schema, json_file, indent=4)

    return FileResponse(
        path=json_filepath,
        media_type="application/json",
        filename=json_filename
    )
