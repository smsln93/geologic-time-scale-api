import re
import csv

from tests.utils.assertions import assert_unit_csv
from tests.utils.export_utils import read_csv_file, is_valid_export_filename


def test_export_pleistocene_csv(client, pleistocene_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/csv")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)
    assert len(rows) == 1  #pleistocene

    pleistocene = rows[0]
    assert_unit_csv(pleistocene,
                    expected_id="pleistocene",
                    expected_name="Pleistocene",
                    expected_rank="Epoch",
                    expected_rank_order=5,
                    expected_begin_time_ma=2.58,
                    expected_begin_uncertainty_ma=0.0,
                    expected_end_time_ma=0.0117,
                    expected_end_uncertainty_ma=0.0,
                    expected_parent_id="")


def test_export_mesozoic_multiple_data_csv(client, mesozoic_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/csv")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)
    assert len(rows) == 4  # mesozoic, jurassic, middle-jurassic, callovian

    mesozoic, jurassic, middle_jurassic, callovian = rows[0], rows[1], rows[2], rows[3]

    assert_unit_csv(mesozoic,
                    expected_id="mesozoic",
                    expected_name="Mesozoic",
                    expected_rank="Era",
                    expected_rank_order=3,
                    expected_begin_time_ma=251.902,
                    expected_begin_uncertainty_ma=0.024,
                    expected_end_time_ma=66.0,
                    expected_end_uncertainty_ma=0.0,
                    expected_parent_id="")

    assert_unit_csv(jurassic,
                    expected_id="jurassic",
                    expected_name="Jurassic",
                    expected_rank="Period",
                    expected_rank_order=4,
                    expected_begin_time_ma=201.4,
                    expected_begin_uncertainty_ma=0.2,
                    expected_end_time_ma=143.1,
                    expected_end_uncertainty_ma=0.6,
                    expected_parent_id="mesozoic")

    assert_unit_csv(middle_jurassic,
                    expected_id="middle-jurassic",
                    expected_name="Middle Jurassic",
                    expected_rank="Epoch",
                    expected_rank_order=5,
                    expected_begin_time_ma=174.7,
                    expected_begin_uncertainty_ma=0.8,
                    expected_end_time_ma=161.5,
                    expected_end_uncertainty_ma=1.0,
                    expected_parent_id="jurassic")

    assert_unit_csv(callovian,
                    expected_id="callovian",
                    expected_name="Callovian",
                    expected_rank="Age",
                    expected_rank_order=6,
                    expected_begin_time_ma=165.3,
                    expected_begin_uncertainty_ma=1.1,
                    expected_end_time_ma=161.5,
                    expected_end_uncertainty_ma=1.0,
                    expected_parent_id="middle-jurassic")


def test_export_csv_empty_data(client, reset_db, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/csv")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)
    assert len(rows) == 0




