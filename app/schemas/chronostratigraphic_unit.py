from typing import Literal

from pydantic import BaseModel, model_validator, ConfigDict

from app.utils.time_value_formatter import format_description_representation


Rank = Literal["Supereon", "Eon", "Era", "Period", "Epoch", "Age"]


class ChronostratigraphicUnitBase(BaseModel):
    name: str
    rank: Rank
    parent_id: str | None

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

        if self.begin_time_ma < self.end_time_ma:
            raise ValueError("Ending time cannot be greater than beginning time")

        if self.rank == "Supereon" and self.parent_id is not None:
            raise ValueError("Supereon cannot have a parent")

        return self


class ChronostratigraphicUnitCreate(ChronostratigraphicUnitBase):
    id: str

    @model_validator(mode="after")
    def validate_create(self):
        if self.parent_id is not None and self.id == self.parent_id:
            raise ValueError(f"Unit cannot be its own parent")

        return self


class ChronostratigraphicUnitRead(ChronostratigraphicUnitBase):
    id: str
    rank_order: int  # Supereon - 1, Eon - 2, Era - 3, Period - 4, Epoch - 5, Age - 6

    model_config = ConfigDict(from_attributes=True)


class ChronostratigraphicUnitUpdate(BaseModel):
    name: str | None = None
    rank: Rank | None = None

    parent_id: str | None = None

    begin_time_ma: float | None = None
    begin_uncertainty_ma: float | None = None
    end_time_ma: float | None = None
    end_uncertainty_ma: float | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_update(self):
        for time, value in {
            "begin_time_ma": self.begin_time_ma,
            "begin_uncertainty_ma": self.begin_uncertainty_ma,
            "end_time_ma": self.end_time_ma,
            "end_uncertainty_ma": self.end_uncertainty_ma}.items():
            if value is not None and value < 0:
                raise ValueError(f"Parameter {time} cannot be a negative value {value}")

        for field_name in self.model_fields_set:
            if field_name != "parent_id" and getattr(self, field_name) is None:
                raise ValueError(f"Field {field_name} cannot be null")

        return self


class ChronostratigraphicUnitReplace(ChronostratigraphicUnitBase):
    begin_uncertainty_ma: float
    end_uncertainty_ma: float


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
