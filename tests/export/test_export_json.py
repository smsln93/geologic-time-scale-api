from tests.utils.assertions import assert_unit_matches_expected_values, assert_units_match_expected
from tests.utils.export_utils import read_json_file, is_valid_export_filename
from tests.utils.expected_units import EXPECTED_UNITS


def test_export_pleistocene_json(client, pleistocene_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)

    assert file.suffix == ".json"
    assert is_valid_export_filename(file)
    assert len(content) == 1
    assert_unit_matches_expected_values(content[0], **EXPECTED_UNITS["pleistocene"])


def test_export_mesozoic_multiple_data_json(client, mesozoic_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)

    assert file.suffix == ".json"
    assert is_valid_export_filename(file)

    expected_ids = {
        "mesozoic", "triassic", "jurassic", "early-jurassic", "middle-jurassic",
        "aalenian", "bajocian", "bathonian", "callovian",
        "late-jurassic", "cretaceous"
    }
    assert_units_match_expected(content, expected_ids, EXPECTED_UNITS)


def test_export_json_empty_data(client, reset_db, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    response = client.get("/geologic-time-scale-api/v1/export/json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)
    assert file.suffix == ".json"
    assert is_valid_export_filename(file)

    assert content == []
