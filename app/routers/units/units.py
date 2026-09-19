from fastapi import Depends, HTTPException, APIRouter, Query
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.security import verify_api_key
from app.database.session import get_db
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from app.schemas.chronostratigraphic_unit import (ChronostratigraphicUnitCreate,
                                                  ChronostratigraphicUnitRead,
                                                  ChronostratigraphicUnitUpdate,
                                                  ChronostratigraphicUnitReplace,
                                                  ChronostratigraphicUnitFormatter,
                                                  ChronostratigraphicUnitService,
                                                  UnitDescription,
                                                  UnitDuration,
                                                  UnitPath, ChronostratigraphicUnitBase)
from app.utils.time_value_formatter import format_duration_representation
from app.enums.rank import Rank


TAG_UNITS_READ = "Geologic Time Scale Units (READ)"
TAG_UNITS_WRITE = "Geologic Time Scale Units (WRITE)"


units_router = APIRouter(
    prefix="/units",
)


def validate_parent_relationship(db: Session, unit_id: str, parent_id: str | None) -> None:
    if parent_id is None:
        return

    if parent_id == unit_id:
        raise HTTPException(status_code=422, detail="Unit cannot be its own parent")

    parent = db.get(ChronostratigraphicUnitDB, parent_id)
    if parent is None:
        raise HTTPException(status_code=422, detail="Parent unit does not exist")

    current_parent = parent
    seen = set()

    while current_parent is not None:
        if current_parent.id == unit_id:
            raise HTTPException(status_code=422, detail="Circular parent relationship")

        if current_parent.id in seen:
            raise HTTPException(status_code=422, detail="Parent hierarchy contains a cycle")

        seen.add(current_parent.id)

        current_parent = (
            db.get(ChronostratigraphicUnitDB, current_parent.parent_id)
            if current_parent.parent_id is not None
            else None
        )


@units_router.get(path="/",
                  tags=[TAG_UNITS_READ],
                  response_model=list[ChronostratigraphicUnitRead],
                  summary="List units",
                  description="Returns all geologic units, optionally filtered " 
                              "by rank, hierarchy, a specific point in time or time boundaries (before/after).")
def get_units(rank: str | None = Query(default=None),
              parent_id: str | None = Query(default=None),
              at_time: float | None = Query(default=None),
              min_age_ma: float | None = Query(default=None),
              max_age_ma: float | None = Query(default=None),
              db: Session = Depends(get_db)):

    if at_time is not None and (min_age_ma is not None or max_age_ma is not None):
        raise HTTPException(
            status_code=400,
            detail="Cannot combine at_time with min_age_ma/max_age_ma"
        )

    if min_age_ma is not None and max_age_ma is not None:
        if min_age_ma >= max_age_ma:
            raise HTTPException(status_code=400, detail="Invalid range: 'min_age_ma' must be less than 'max_age_ma'")

    query = db.query(ChronostratigraphicUnitDB).order_by(
        ChronostratigraphicUnitDB.begin_time_ma.desc(),
        ChronostratigraphicUnitDB.rank_order.asc(),
        ChronostratigraphicUnitDB.id.asc()
    )

    if rank is not None:
        rank = rank.strip()
        if rank:
            query = query.filter(ChronostratigraphicUnitDB.rank == rank)

    if parent_id is not None:
        parent_id = parent_id.strip()
        if parent_id:
            query = query.filter(ChronostratigraphicUnitDB.parent_id == parent_id)

    if at_time is not None:
        query = query.filter(ChronostratigraphicUnitDB.begin_time_ma >= at_time,
                             ChronostratigraphicUnitDB.end_time_ma < at_time)

    if min_age_ma is not None:
        query = query.filter(ChronostratigraphicUnitDB.end_time_ma >= min_age_ma)

    if max_age_ma is not None:
        query = query.filter(ChronostratigraphicUnitDB.begin_time_ma <= max_age_ma)

    return query.all()


@units_router.get(path="/{unit_id}",
                  tags=[TAG_UNITS_READ],
                  response_model=ChronostratigraphicUnitRead,
                  summary="Get unit",
                  description="Returns detailed information about a geologic unit")
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return unit


@units_router.get(path="/{unit_id}/description",
                  tags=[TAG_UNITS_READ],
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


@units_router.get(path="/{unit_id}/child_units",
                  tags=[TAG_UNITS_READ],
                  response_model=list[ChronostratigraphicUnitRead],
                  summary="Get child units",
                  description="Returns all lower-level geologic subdivisions (e.g. Era → Periods)")
def get_child_units(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return [ChronostratigraphicUnitRead.model_validate(child) for child in unit.children]


@units_router.get(path="/{unit_id}/parent_unit",
                  tags=[TAG_UNITS_READ],
                  response_model=ChronostratigraphicUnitRead,
                  summary="Get parent unit",
                  description="Returns the immediate higher-level geologic unit (e.g. Period → Era)")
def get_parent_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    if not unit.parent_id:
        raise HTTPException(status_code=404, detail="Parent unit not found")

    parent_unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit.parent_id).first()
    return ChronostratigraphicUnitRead.model_validate(parent_unit)


@units_router.get(path="/{unit_id}/path",
                  tags=[TAG_UNITS_READ],
                  response_model=UnitPath,
                  summary="Get unit lineage path",
                  description="Returns full hierarchical path from the root (e.g. Eon → Era → Period → Epoch)")
def get_unit_path(unit_id: str, db: Session = Depends(get_db)):
    units = db.query(ChronostratigraphicUnitDB).all()

    unit_map = {
        unit.id: unit for unit in units
    }

    path: list[str] = []
    current = unit_map.get(unit_id)

    if current is None:
        raise HTTPException(status_code=404, detail="Unit not found")

    seen = set()

    while current is not None:
        if current.id in seen:
            raise HTTPException(status_code=409, detail="Parent hierarchy contains a cycle")

        seen.add(current.id)
        path.append(current.name)

        if current.parent_id is None:
            break

        parent = unit_map.get(current.parent_id)

        if parent is None:
            raise HTTPException(status_code=409, detail="Parent unit does not exist")

        current = parent

    return UnitPath(id=unit_id, name=path[0], path=list(reversed(path)))


@units_router.get(path="/{unit_id}/duration",
                  tags=[TAG_UNITS_READ],
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


@units_router.post(path="/",
                   tags=[TAG_UNITS_WRITE],
                   dependencies=[Depends(verify_api_key)],
                   response_model=ChronostratigraphicUnitRead,
                   status_code=201,
                   summary="Create unit",
                   description="Returns newly created unit")
def create_unit(payload: ChronostratigraphicUnitCreate, db: Session = Depends(get_db)):

    validate_parent_relationship(db, payload.id, payload.parent_id)

    unit = ChronostratigraphicUnitDB(**payload.model_dump())
    unit.rank_order = Rank(unit.rank).order
    db.add(unit)

    try:
        db.commit()
        db.refresh(unit)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Unit already exists")

    return unit

@units_router.put(path="/{unit_id}",
                  tags=[TAG_UNITS_WRITE],
                  dependencies=[Depends(verify_api_key)],
                  response_model=ChronostratigraphicUnitRead,
                  summary="Replace all data in unit",
                  description="Returns replaced unit")
def replace_unit(unit_id: str, payload: ChronostratigraphicUnitReplace, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    validate_parent_relationship(db, unit_id, payload.parent_id)

    new_data = payload.model_dump()

    for key, value in new_data.items():
        setattr(unit, key, value)

    unit.rank_order = Rank(unit.rank).order

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database constraint violation")

    db.refresh(unit)

    return unit


@units_router.patch(path="/{unit_id}",
                    tags=[TAG_UNITS_WRITE],
                    dependencies=[Depends(verify_api_key)],
                    response_model=ChronostratigraphicUnitRead,
                    summary="Update parts of the unit",
                    description="Returns updated unit")
def update_unit(unit_id: str, payload: ChronostratigraphicUnitUpdate, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    update_data = payload.model_dump(exclude_unset=True, mode="json")

    current_data = ChronostratigraphicUnitRead.model_validate(unit).model_dump(exclude={"id", "rank_order"}, mode="json")

    merged_data = {**current_data, **update_data}

    try:
        ChronostratigraphicUnitBase.model_validate(merged_data)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors(include_input=False, include_context=False)) from err

    if "parent_id" in update_data:
        validate_parent_relationship(db, unit_id, update_data["parent_id"])

    for key, value in update_data.items():
        setattr(unit, key, value)

    if "rank" in update_data:
        unit.rank_order = Rank(unit.rank).order

    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database constraint violation") from err

    db.refresh(unit)

    return unit


@units_router.delete(path="/{unit_id}",
                     tags=[TAG_UNITS_WRITE],
                     dependencies=[Depends(verify_api_key)],
                     status_code=204,
                     summary="Delete unit",
                     description="Deletes unit")
def delete_unit(unit_id: str, db: Session = Depends(get_db)):

    unit = db.query(ChronostratigraphicUnitDB).filter_by(id=unit_id).first()

    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    if unit.children:
        raise HTTPException(status_code=400, detail="Cannot delete unit with child units")

    db.delete(unit)
    db.commit()
