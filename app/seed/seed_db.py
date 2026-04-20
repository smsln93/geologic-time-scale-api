import json
from pathlib import Path

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB


def seed_db(session):
    base_path = Path(__file__).parent.joinpath("input")

    files = ["precambrian.json",
             "hadean.json",
             "archean.json",
             "proterozoic.json",
             "phanerozoic.json",
             "paleozoic.json",
             "mesozoic.json",
             "cenozoic.json"]

    for file in files:
        with open(base_path.joinpath(file), "r") as json_file:
            data = json.load(json_file)

        for item in data:
            print(type(data), data)
            print(type(item), item)
            session.add(ChronostratigraphicUnitDB(**item))

    session.commit()