from typing import Optional, Dict

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.schemas.chronostratigraphic_unit import ChronostratigraphicUnitBase
from app.utils.time_value_formatter import format_duration_representation
from app.api.router import api_router


@api_router.get(path="/units",
                tags=["Geologic Time Scale Units"],
                summary="List units",
                description="Returns all geologic units, optionally filtered "
                            "by rank, hierarchy, a specific point in time or time boundaries (before/after).")
def get_units(rank: Optional[str] = None,
              parent_id: Optional[str] = None,
              at_time: Optional[float] = None,
              before: Optional[float] = None,
              after: Optional[float] = None,
              db: Session = Depends(get_db)):

    query = db.query(ChronostratigraphicUnitDB)

    if at_time is not None and (before is not None or after is not None):
        raise HTTPException(
            status_code=400,
            detail="Cannot combine at_time with older_than/younger_than"
        )

    if rank not in (None, "", " "):
        query = query.filter(ChronostratigraphicUnitDB.rank == rank)

    if parent_id not in (None, "", " "):
        query = query.filter(ChronostratigraphicUnitDB.parent_id == parent_id)

    if at_time not in (None, "", " "):
        query = query.filter(ChronostratigraphicUnitDB.begin_time_ma > at_time,
                             ChronostratigraphicUnitDB.end_time_ma <= at_time)

    if before not in (None, "", " "):
        query = query.filter(ChronostratigraphicUnitDB.begin_time_ma > before)

    if after not in (None, "", " "):
        query = query.filter(ChronostratigraphicUnitDB.end_time_ma < after)

    return query.all()


@api_router.get(path="/units/{unit_id}",
                tags=["Geologic Time Scale Units"],
                summary="Get unit",
                description="Returns detailed information about a geologic unit")
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    query = db.query(ChronostratigraphicUnitDB)
    query = query.filter(ChronostratigraphicUnitDB.id == unit_id)
    return query.all()


@api_router.get(path="/units/{unit_id}/description",
                tags=["Geologic Time Scale Units"],
                summary="Get unit description",
                description="Returns the description of the geologic unit")
def get_unit_description(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter(ChronostratigraphicUnitDB.id == unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit_schema = ChronostratigraphicUnitBase.model_validate(unit)

    return unit_schema.description


@api_router.get(path="/units/{unit_id}/child_units",
                tags=["Geologic Time Scale Units"],
                summary="Get child units",
                description="Returns all lower-level geologic subdivisions (e.g. Era → Periods)")
def get_child_units(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return unit.children


@api_router.get(path="/units/{unit_id}/parent_unit",
                tags=["Geologic Time Scale Units"],
                summary="Get parent unit",
                description="Returns the immediate higher-level geologic unit (e.g. Period → Era)")
def get_parent_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return unit.parent


@api_router.get(path="/units/{unit_id}/path",
                tags=["Geologic Time Scale Units"],
                summary="Get unit lineage path",
                description="Returns full hierarchical path from the root (e.g. Eon → Era → Period → Epoch)")
def get_unit_path(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    path: Dict[str, str] = {}

    current = unit

    while current:
        path[current.rank] = current.name
        current = current.parent

    return path


@api_router.get(path="/units/{unit_id}/duration",
                tags=["Geologic Time Scale Units"],
                summary="Get unit duration",
                description="Returns the time span of the unit")
def get_unit_duration(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit_schema = ChronostratigraphicUnitBase.model_validate(unit)
    return format_duration_representation(unit_schema.duration_ma)
