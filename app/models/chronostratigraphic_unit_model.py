from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class ChronostratigraphicUnitDB(Base):
    __tablename__ = "chronostratigraphic_units"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(String)  # supereon, eon, era, period, epoch, age
    rank_order = Column(Integer, nullable=False)

    begin_time_ma = Column(Float, nullable=False)
    begin_uncertainty_ma = Column(Float, nullable=False, default=0.0)

    end_time_ma = Column(Float, nullable=False)
    end_uncertainty_ma = Column(Float, nullable=False, default=0.0)

    parent_id = Column(String, ForeignKey("chronostratigraphic_units.id"))

    parent = relationship(
        argument="ChronostratigraphicUnitDB",
        remote_side=[id],
        back_populates="children"
    )

    children = relationship(
        argument="ChronostratigraphicUnitDB",
        back_populates="parent"
    )
