from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.services.export_service import ExportService


export_router = APIRouter(prefix="/export", tags=["Export"])


@export_router.get(path="/csv",
                   summary="Export units to CSV",
                   description="Exports all geologic units as a downloadable CSV file")
def export_units_csv(db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()
    if not units:
        raise HTTPException(status_code=404, detail="No data available to export")

    csv_filepath = ExportService.export_units_to_csv(units)

    return FileResponse(
        path=csv_filepath,
        media_type="text/csv",
        filename=csv_filepath.name
    )


@export_router.get(path="/json",
                   summary="Export units to JSON",
                   description="Exports all geologic units as a downloadable JSON file")
def export_units_json(db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()
    if not units:
        raise HTTPException(status_code=404, detail="No seed to export")

    json_filepath = ExportService.export_units_to_json(units)

    return FileResponse(
        path=json_filepath,
        media_type="application/json",
        filename=json_filepath.name
    )
