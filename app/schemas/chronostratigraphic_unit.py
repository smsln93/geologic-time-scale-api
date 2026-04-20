from typing import Literal, Optional, List

from pydantic import BaseModel, model_validator, ConfigDict

from app.utils.time_value_formatter import format_description_representation
from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB

class ChronostratigraphicUnitCreate(BaseModel):
    id: str
    name: str
    rank: Literal["Supereon", "Eon", "Era", "Period", "Epoch", "Age"]

    parent_id: Optional[str] = None

    begin_time_ma: float
    begin_uncertainty_ma: float = 0.0
    end_time_ma: float
    end_uncertainty_ma: float = 0.0

    @model_validator(mode="after")
    def validate(self):
        for time, value in {
            "begin_time_ma": self.begin_time_ma,
            "begin_uncertainty_ma": self.begin_uncertainty_ma,
            "end_time_ma": self.end_time_ma,
            "end_uncertainty_ma": self.end_uncertainty_ma}.items():
            if value < 0:
                raise ValueError(f"Parameter {time} cannot be a negative value {value}")

        if self.parent_id is not None and self.id == self.parent_id:
            raise ValueError(f"Unit cannot be its own parent")

        if self.rank == "Supereon" and self.parent_id is not None:
            raise ValueError("Supereon cannot have a parent")

        if self.begin_time_ma < self.end_time_ma:
            raise ValueError("Ending time cannot be greater than beginning time")

        return self


class ChronostratigraphicUnitRead(BaseModel):
    id: str
    name: str
    rank: Literal["Supereon", "Eon", "Era", "Period", "Epoch", "Age"]
    rank_order: int  # Supereon - 1, Eon - 2, Era - 3, Period - 4, Epoch - 5, Age - 6

    parent_id: Optional[str] = None

    begin_time_ma: float
    begin_uncertainty_ma: float = 0.0
    end_time_ma: float
    end_uncertainty_ma: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class UnitDescription(BaseModel):
    description: str


class UnitDuration(BaseModel):
    duration_ma: float
    formatted_duration: str


class UnitPath(BaseModel):
    id: str
    name: str
    path: list[str]


class ChronostratigraphicUnitService:

    @staticmethod
    def contains_unit(unit: ChronostratigraphicUnitRead, other: ChronostratigraphicUnitRead) -> bool:
        return unit.begin_time_ma >= other.begin_time_ma and unit.end_time_ma <= other.end_time_ma

    @staticmethod
    def contains_age_ma(unit: ChronostratigraphicUnitRead, age_ma: float) -> bool:
        return unit.begin_time_ma >= age_ma > unit.end_time_ma

    @staticmethod
    def duration_ma(unit: ChronostratigraphicUnitRead) -> float:
        return max(0.0, unit.begin_time_ma - unit.end_time_ma)


class ChronostratigraphicUnitFormatter:

    @staticmethod
    def description(unit: ChronostratigraphicUnitRead) -> str:
        unit_begins = format_description_representation(unit.begin_time_ma, unit.begin_uncertainty_ma)
        unit_ends = format_description_representation(unit.end_time_ma, unit.end_uncertainty_ma)

        return f"{unit.name} - {unit.rank} lasted from {unit_begins} to {unit_ends}"
