from tests.utils.assertions import assert_unit
from tests.utils.export_utils import read_json_file, is_valid_export_filename


def test_export_pleistocene_json(client, pleistocene_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/json")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)

    assert file.suffix == ".json"
    assert is_valid_export_filename(file)

    assert isinstance(content, list)
    assert len(content) == 1

    pleistocene = content[0]

    assert_unit(pleistocene,
                expected_id="pleistocene",
                expected_name="Pleistocene",
                expected_rank="Epoch",
                expected_rank_order=5,
                expected_begin_time_ma=2.58,
                expected_begin_uncertainty_ma=0.0,
                expected_end_time_ma=0.0117,
                expected_end_uncertainty_ma=0.0,
                expected_parent_id=None)


def test_export_mesozoic_multiple_data_json(client, mesozoic_unit, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/json")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)

    assert file.suffix == ".json"
    assert is_valid_export_filename(file)

    assert isinstance(content, list)
    assert len(content) == 4


    mesozoic, jurassic, middle_jurassic, callovian = content[0], content[1], content[2], content[3]

    assert_unit(mesozoic,
                expected_id="mesozoic",
                expected_name="Mesozoic",
                expected_rank="Era",
                expected_rank_order=3,
                expected_begin_time_ma=251.902,
                expected_begin_uncertainty_ma=0.024,
                expected_end_time_ma=66.0,
                expected_end_uncertainty_ma=0.0,
                expected_parent_id=None)


    assert_unit(jurassic,
                expected_id="jurassic",
                expected_name="Jurassic",
                expected_rank="Period",
                expected_rank_order=4,
                expected_begin_time_ma=201.4,
                expected_begin_uncertainty_ma=0.2,
                expected_end_time_ma=143.1,
                expected_end_uncertainty_ma=0.6,
                expected_parent_id="mesozoic")


    assert_unit(middle_jurassic,
                expected_id="middle-jurassic",
                expected_name="Middle Jurassic",
                expected_rank="Epoch",
                expected_rank_order=5,
                expected_begin_time_ma=174.7,
                expected_begin_uncertainty_ma=0.8,
                expected_end_time_ma=161.5,
                expected_end_uncertainty_ma=1.0,
                expected_parent_id="jurassic")

    assert_unit(callovian,
                expected_id="callovian",
                expected_name="Callovian",
                expected_rank="Age",
                expected_rank_order=6,
                expected_begin_time_ma=165.3,
                expected_begin_uncertainty_ma=1.1,
                expected_end_time_ma=161.5,
                expected_end_uncertainty_ma=1.0,
                expected_parent_id="middle-jurassic")


def test_export_json_empty_data(client, reset_db, tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.export_service.EXPORT_DIR", tmp_path)

    res = client.get("/geologic-time-scale-api/v1/export/json")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("application/json")

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    content, file = read_json_file(tmp_path)
    assert file.suffix == ".json"
    assert is_valid_export_filename(file)

    assert isinstance(content, list)
    assert len(content) == 0

