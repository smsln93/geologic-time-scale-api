from tests.utils.assertions import assert_unit_csv_match_expected_values
from tests.utils.export_utils import read_csv_file, is_valid_export_filename
from tests.utils.expected_units import EXPECTED_UNITS


def test_export_pleistocene_csv(client, pleistocene_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)
    assert len(rows) == 1
    assert_unit_csv_match_expected_values(rows[0], **EXPECTED_UNITS["pleistocene"])


def test_export_mesozoic_multiple_data_csv(client, mesozoic_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)

    expected_ids = {
        "mesozoic", "triassic", "jurassic", "early-jurassic", "middle-jurassic",
        "aalenian", "bajocian", "bathonian", "callovian",
        "late-jurassic", "cretaceous"
    }

    rows_by_id = {row["id"]: row for row in rows}

    assert len(rows) == len(expected_ids)
    assert set(rows_by_id) == expected_ids

    for unit_id in expected_ids:
        assert_unit_csv_match_expected_values(
            rows_by_id[unit_id], **EXPECTED_UNITS[unit_id]
        )


def test_export_csv_empty_data(client, reset_db, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")

    rows, file = read_csv_file(tmp_path)
    assert file.suffix == ".csv"
    assert is_valid_export_filename(file)
    assert rows == []
