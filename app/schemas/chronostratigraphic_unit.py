from typing import Literal, Optional

from pydantic import BaseModel, model_validator, ConfigDict

from app.utils.time_value_formatter import format_description_representation


class ChronostratigraphicUnitCreate(BaseModel):
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

    @property
    def duration_ma(self) -> float:
        return round(max(0.0, self.begin_time_ma - self.end_time_ma),3)

    @property
    def description(self) -> str:
        unit_begins = format_description_representation(self.begin_time_ma, self.begin_uncertainty_ma)
        unit_ends = format_description_representation(self.end_time_ma, self.end_uncertainty_ma)

        return f"{self.name} - {self.rank} lasted from {unit_begins} to {unit_ends}"


class ChronostratigraphicUnitUpdate(BaseModel):
    name: Optional[str] = None
    rank: Optional[str] = None
    rank_order: Optional[int]

    parent_id: Optional[str] = None

    begin_time_ma: Optional[float] = None
    begin_uncertainty_ma: Optional[float] = None
    end_time_ma: Optional[float] = None
    end_uncertainty_ma: Optional[float] = None


class ChronostratigraphicUnitService:

    @staticmethod
    def contains_unit(unit, other) -> bool:
        return unit.begin_time_ma >= other.begin_time_ma and unit.end_time_ma <= other.end_time_ma

    @staticmethod
    def contains_age_ma(unit, age_ma: float) -> bool:
        return unit.begin_time_ma >= age_ma > unit.end_time_ma


