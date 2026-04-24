import pytest

from tests.utils.assertions import assert_unit, assert_unit_has_required_properties


def test_get_pleistocene_epoch(client, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/pleistocene")
    assert res.status_code == 200

    unit = res.json()
    assert isinstance(unit, dict)

    assert_unit_has_required_properties(unit)
    assert_unit(unit,
                expected_id="pleistocene",
                expected_name="Pleistocene",
                expected_rank="Epoch",
                expected_rank_order=5,
                expected_begin_time_ma=2.58,
                expected_begin_uncertainty_ma=0.0,
                expected_end_time_ma=0.0117,
                expected_end_uncertainty_ma=0.0,
                expected_parent_id=None)


def test_unit_by_id_not_found(client, mesozoic_unit, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/nonexistent")
    assert res.status_code == 404


def test_get_list_of_all_units(client, mesozoic_unit, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert len(units) == 5  # mesozoic, jurassic, middle-jurassic, callovian, pleistocene

    for unit in units:
        assert isinstance(unit, dict)
        assert_unit_has_required_properties(unit)
        assert unit.get("id") in ["mesozoic", "jurassic", "middle-jurassic", "callovian", "pleistocene"]

        if unit.get("id") == "mesozoic":
            assert_unit(unit,
                        expected_id="mesozoic",
                        expected_name="Mesozoic",
                        expected_rank="Era",
                        expected_rank_order=3,
                        expected_begin_time_ma=251.902,
                        expected_begin_uncertainty_ma=0.024,
                        expected_end_time_ma=66.0,
                        expected_end_uncertainty_ma=0.0,
                        expected_parent_id=None)

        if unit.get("id") == "jurassic":
            assert_unit(unit,
                        expected_id="jurassic",
                        expected_name="Jurassic",
                        expected_rank="Period",
                        expected_rank_order=4,
                        expected_begin_time_ma=201.4,
                        expected_begin_uncertainty_ma=0.2,
                        expected_end_time_ma=143.1,
                        expected_end_uncertainty_ma=0.6,
                        expected_parent_id="mesozoic")

        if unit.get("id") == "middle-jurassic":
            assert_unit(unit,
                        expected_id="middle-jurassic",
                        expected_name="Middle Jurassic",
                        expected_rank="Epoch",
                        expected_rank_order=5,
                        expected_begin_time_ma=174.7,
                        expected_begin_uncertainty_ma=0.8,
                        expected_end_time_ma=161.5,
                        expected_end_uncertainty_ma=1.0,
                        expected_parent_id="jurassic")

        if unit.get("id") == "callovian":
            assert_unit(unit,
                        expected_id="callovian",
                        expected_name="Callovian",
                        expected_rank="Age",
                        expected_rank_order=6,
                        expected_begin_time_ma=165.3,
                        expected_begin_uncertainty_ma=1.1,
                        expected_end_time_ma=161.5,
                        expected_end_uncertainty_ma=1.0,
                        expected_parent_id="middle-jurassic")

            if unit.get("id") == "pleistocene":
                assert_unit(unit,
                            expected_id="pleistocene",
                            expected_name="Pleistocene",
                            expected_rank="Epoch",
                            expected_rank_order=5,
                            expected_begin_time_ma=2.58,
                            expected_begin_uncertainty_ma=0.0,
                            expected_end_time_ma=0.0117,
                            expected_end_uncertainty_ma=0.0,
                            expected_parent_id=None)


def test_get_empty_list(client, reset_db):
    res = client.get("/geologic-time-scale-api/v1/units/")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert units == []


def test_units_filter_by_rank(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?rank=Age")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert len(units) == 1

    unit = units[0]
    assert isinstance(unit, dict)
    assert_unit_has_required_properties(unit)

    assert_unit(unit,
            expected_id="callovian",
            expected_name="Callovian",
            expected_rank="Age",
            expected_rank_order=6,
            expected_begin_time_ma=165.3,
            expected_begin_uncertainty_ma=1.1,
            expected_end_time_ma=161.5,
            expected_end_uncertainty_ma=1.0,
            expected_parent_id="middle-jurassic")


def test_units_filter_by_parent_id(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?parent_id=jurassic")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert len(units) == 1

    unit = units[0]
    assert isinstance(unit, dict)
    assert_unit_has_required_properties(unit)

    assert_unit(unit,
                expected_id="middle-jurassic",
                expected_name="Middle Jurassic",
                expected_rank="Epoch",
                expected_rank_order=5,
                expected_begin_time_ma=174.7,
                expected_begin_uncertainty_ma=0.8,
                expected_end_time_ma=161.5,
                expected_end_uncertainty_ma=1.0,
                expected_parent_id="jurassic")


def test_units_filter_by_before(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?before=160.0")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert len(units) == 2  # middle-jurassic, callovian

    for unit in units:
        assert isinstance(unit, dict)
        assert_unit_has_required_properties(unit)
        assert unit.get("id") in ["middle-jurassic", "callovian"]

        if unit.get("id") == "middle-jurassic":
            assert_unit(unit,
                        expected_id="middle-jurassic",
                        expected_name="Middle Jurassic",
                        expected_rank="Epoch",
                        expected_rank_order=5,
                        expected_begin_time_ma=174.7,
                        expected_begin_uncertainty_ma=0.8,
                        expected_end_time_ma=161.5,
                        expected_end_uncertainty_ma=1.0,
                        expected_parent_id="jurassic")

        if unit.get("id") == "callovian":
            assert_unit(unit,
                        expected_id="callovian",
                        expected_name="Callovian",
                        expected_rank="Age",
                        expected_rank_order=6,
                        expected_begin_time_ma=165.3,
                        expected_begin_uncertainty_ma=1.1,
                        expected_end_time_ma=161.5,
                        expected_end_uncertainty_ma=1.0,
                        expected_parent_id="middle-jurassic")


def test_before_filter_excludes_exact_boundary(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?before=161.5")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    unit_ids = [unit["id"] for unit in units]

    assert "callovian" not in unit_ids
    assert "middle-jurassic" not in unit_ids
    assert "jurassic" not in unit_ids
    assert "mesozoic" not in unit_ids


def test_units_filter_by_after(client, mesozoic_unit, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?after=170.0")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    assert len(units) == 2  # callovian, pleistocene

    for unit in units:
        assert isinstance(unit, dict)
        assert_unit_has_required_properties(unit)
        assert unit.get("id") in ["callovian", "pleistocene"]

        if unit.get("id") == "callovian":
            assert_unit(unit,
                        expected_id="callovian",
                        expected_name="Callovian",
                        expected_rank="Age",
                        expected_rank_order=6,
                        expected_begin_time_ma=165.3,
                        expected_begin_uncertainty_ma=1.1,
                        expected_end_time_ma=161.5,
                        expected_end_uncertainty_ma=1.0,
                        expected_parent_id="middle-jurassic")

            if unit.get("id") == "pleistocene":
                assert_unit(unit,
                            expected_id="pleistocene",
                            expected_name="Pleistocene",
                            expected_rank="Epoch",
                            expected_rank_order=5,
                            expected_begin_time_ma=2.58,
                            expected_begin_uncertainty_ma=0.0,
                            expected_end_time_ma=0.0117,
                            expected_end_uncertainty_ma=0.0,
                            expected_parent_id=None)


def test_after_filter_excludes_exact_boundary(client, mesozoic_unit, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/?after=161.5")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)
    unit_ids = [unit["id"] for unit in units]

    assert "callovian" not in unit_ids
    assert "pleistocene" in unit_ids


def test_get_jurassic_parent_as_mesozoic(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/jurassic/parent_unit")
    assert res.status_code == 200

    unit = res.json()
    assert isinstance(unit, dict)
    assert_unit_has_required_properties(unit)
    assert_unit(unit,
                expected_id="mesozoic",
                expected_name="Mesozoic",
                expected_rank="Era",
                expected_rank_order=3,
                expected_begin_time_ma=251.902,
                expected_begin_uncertainty_ma=0.024,
                expected_end_time_ma=66.0,
                expected_end_uncertainty_ma=0.0,
                expected_parent_id=None)


def test_get_parent_if_unit_has_none(client, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/pleistocene/parent_unit")
    assert res.status_code == 404


def test_get_mesozoic_children(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/mesozoic/child_units")
    assert res.status_code == 200

    units = res.json()
    assert isinstance(units, list)

    for unit in units:
        assert isinstance(unit, dict)
        assert_unit_has_required_properties(unit)

        assert_unit(unit,
                    expected_id="jurassic",
                    expected_name="Jurassic",
                    expected_rank="Period",
                    expected_rank_order=4,
                    expected_begin_time_ma=201.4,
                    expected_begin_uncertainty_ma=0.2,
                    expected_end_time_ma=143.1,
                    expected_end_uncertainty_ma=0.6,
                    expected_parent_id="mesozoic")


def test_check_if_no_children_returns_empty_list(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/callovian/child_units")
    assert res.status_code == 200

    unit = res.json()
    assert isinstance(unit, list)
    assert unit == []


def test_get_jurassic_duration(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/jurassic/duration")
    assert res.status_code == 200

    unit_duration = res.json()
    assert isinstance(unit_duration, dict)

    assert unit_duration.get("duration_ma") == pytest.approx(58.300)
    assert unit_duration.get("formatted_duration") == "58.300 Ma"


def test_get_duration_of_nonexistent_unit(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/nonexistent_unit/duration")
    assert res.status_code == 404


def test_get_pleistocene_description(client, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/pleistocene/description")
    assert res.status_code == 200

    unit_description = res.json()
    assert isinstance(unit_description, dict)

    assert unit_description.get("description") == "Pleistocene - Epoch lasted from 2.58 Ma to 11.7 ka"


def test_get_callovian_path(client, mesozoic_unit):
    res = client.get("/geologic-time-scale-api/v1/units/callovian/path")
    assert res.status_code == 200

    unit_path = res.json()
    assert isinstance(unit_path, dict)

    assert unit_path["path"] == ["Mesozoic", "Jurassic", "Middle Jurassic", "Callovian"]
