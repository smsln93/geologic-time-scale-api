from typing import Optional, Dict, List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.security import verify_api_key
from app.database.session import get_db
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.schemas.chronostratigraphic_unit import (ChronostratigraphicUnitCreate, ChronostratigraphicUnitRead,
                                                  UnitDescription, UnitDuration, UnitPath,
                                                  ChronostratigraphicUnitFormatter, ChronostratigraphicUnitService)
from app.utils.time_value_formatter import format_duration_representation
from app.api.router import api_router


@api_router.get(path="/units",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=List[ChronostratigraphicUnitRead],
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
            detail="Cannot combine at_time with before/after"
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

    if before is not None and after is not None:
        if before >= after:
            raise HTTPException(status_code=400, detail="Invalid range: 'after' must be greater than 'before'")

    return query.all()


@api_router.get(path="/units/{unit_id}",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=ChronostratigraphicUnitRead,
                summary="Get unit",
                description="Returns detailed information about a geologic unit")
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return unit


@api_router.get(path="/units/{unit_id}/description",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=UnitDescription,
                summary="Get unit description",
                description="Returns the description of the geologic unit")
def get_unit_description(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit_read = ChronostratigraphicUnitRead.model_validate(unit)
    unit_description = ChronostratigraphicUnitFormatter.description(unit_read)

    return UnitDescription(description=unit_description)


@api_router.get(path="/units/{unit_id}/child_units",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=List[ChronostratigraphicUnitRead],
                summary="Get child units",
                description="Returns all lower-level geologic subdivisions (e.g. Era → Periods)")
def get_child_units(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return [ChronostratigraphicUnitRead.model_validate(child) for child in unit.children]


@api_router.get(path="/units/{unit_id}/parent_unit",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=ChronostratigraphicUnitRead,
                summary="Get parent unit",
                description="Returns the immediate higher-level geologic unit (e.g. Period → Era)")
def get_parent_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return unit.parent


@api_router.get(path="/units/{unit_id}/path",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=UnitPath,
                summary="Get unit lineage path",
                description="Returns full hierarchical path from the root (e.g. Eon → Era → Period → Epoch)")
def get_unit_path(unit_id: str, db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()

    unit_map = {
        unit.id: unit for unit in units
    }

    path: List[str] = []
    current = unit_map.get(unit_id)

    if not current:
        raise HTTPException(status_code=404, detail="Unit not found")

    while current:
        path.append(current.name)
        current = unit_map.get(current.parent_id)
        if not current:
            break

    return UnitPath(id=unit_id , name=path[0], path=list(reversed(path)))


@api_router.get(path="/units/{unit_id}/duration",
                tags=["Geologic Time Scale Units (READ)"],
                response_model=UnitDuration,
                summary="Get unit duration",
                description="Returns the time span of the unit")
def get_unit_duration(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit_read = ChronostratigraphicUnitRead.model_validate(unit)
    unit_duration = ChronostratigraphicUnitService.duration_ma(unit_read)
    return UnitDuration(duration_ma=unit_duration,
                        formatted_duration=format_duration_representation(unit_duration))


@api_router.post(path="/units",
                 tags=["Geologic Time Scale Units (WRITE)"],
                 dependencies=[Depends(verify_api_key)],
                 response_model=ChronostratigraphicUnitRead,
                 summary="Create unit",
                 description="Returns newly created unit")
def create_unit(payload: ChronostratigraphicUnitCreate, db: Session = Depends(get_db)):

    unit = ChronostratigraphicUnitDB(**payload.model_dump())

    db.add(unit)
    db.commit()
    db.refresh(unit)

    return unit

@api_router.put(path="/units/{unit_id}",
                tags=["Geologic Time Scale Units (WRITE)"],
                dependencies=[Depends(verify_api_key)],
                response_model=ChronostratigraphicUnitRead,
                summary="Update unit",
                description="Returns updated unit")
def update_unit(unit_id: str, payload: ChronostratigraphicUnitCreate, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    for key, value in payload.model_dump().items():
        setattr(unit, key, value)

    db.commit()
    db.refresh(unit)

    return unit


@api_router.patch(path="/units/{unit_id}",
                  tags=["Geologic Time Scale Units (WRITE)"],
                  dependencies=[Depends(verify_api_key)],
                  response_model=ChronostratigraphicUnitRead,
                  summary="Update parts of the unit",
                  description="Returns updated unit")
def update_unit(unit_id: str, payload: ChronostratigraphicUnitCreate, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(unit, key, value)

    db.commit()
    db.refresh(unit)

    return unit


@api_router.delete(path="/units/{unit_id}",
                   tags=["Geologic Time Scale Units (WRITE)"],
                   dependencies=[Depends(verify_api_key)],
                   summary="Delete unit",
                   description="Deletes unit")
def update_unit(unit_id: str, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    if unit.children:
        raise HTTPException(status_code=400, detail="Cannot delete unit with child units")

    db.delete(unit)
    db.commit()

    return {"deleted_id": unit_id}
