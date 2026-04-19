from typing import Literal, Optional

from pydantic import BaseModel, model_validator, ConfigDict

from app.utils.time_value_formatter import format_description_representation


class ChronostratigraphicUnitBase(BaseModel):
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

    @model_validator(mode="after")
    def validate(self):
        for time, value in {
            "begin_time_ma": self.begin_time_ma,
            "begin_uncertainty_ma": self.begin_uncertainty_ma,
            "end_time_ma": self.end_time_ma,
            "end_uncertainty_ma": self.end_uncertainty_ma}.items():
            if value < 0:
                raise ValueError(f"{self.id} parameter {time} cannot be a negative value {value}")

        if self.begin_time_ma < self.end_time_ma:
            raise ValueError("Ending time cannot be greater than beginning time")

        if self.parent_id is not None and self.id == self.parent_id:
            raise ValueError("Unit cannot be its own parent")

        return self

    def get_parent_id(self) -> Optional[str]:
        return self.parent_id

    @property
    def duration_ma(self) -> float:
        return round(max(0.0, self.begin_time_ma - self.end_time_ma),3)

    @property
    def description(self) -> str:
        unit_begins = format_description_representation(self.begin_time_ma, self.begin_uncertainty_ma)
        unit_ends = format_description_representation(self.end_time_ma, self.end_uncertainty_ma)

        return f"{self.name} - {self.rank} lasted from {unit_begins} to {unit_ends}"

    def contains_unit(self, other: ChronostratigraphicUnitBase) -> bool:
        return self.begin_time_ma >= other.begin_time_ma and self.end_time_ma <= other.end_time_ma

    def contains_age_ma(self, age_ma: float) -> bool:
        return self.begin_time_ma >= age_ma > self.end_time_ma

    def to_json_dict(self) -> dict:
        return self.model_dump(mode="json")

    def __str__(self) -> str:
        return self.description

    def __repr__(self) -> str:
        return (f"ChronostratigraphicUnit(id={self.id}, name={self.name}, rank={self.rank}, parent_id={self.parent_id}, "
                f"begin_time_ma={self.begin_time_ma}, end_time_ma={self.end_time_ma}, description={self.description})")
