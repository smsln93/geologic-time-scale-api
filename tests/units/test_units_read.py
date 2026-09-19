import pytest

from app.models.chronostratigraphic_unit_model import ChronostratigraphicUnitDB
from tests.utils.assertions import (assert_unit_matches_expected_values,
                                    assert_unit_has_required_properties,
                                    assert_units_match_expected)
from tests.utils.expected_units import EXPECTED_UNITS


def test_get_list_of_all_units(client, mesozoic_unit, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/")
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"mesozoic", "triassic", "jurassic", "early-jurassic", "middle-jurassic",
                    "aalenian", "bajocian", "bathonian", "callovian", "late-jurassic",
                    "cretaceous", "pleistocene"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_get_units_from_empty_database(client, reset_db):
    response = client.get("/geologic-time-scale-api/v1/units/")
    assert response.status_code == 200
    assert response.json() == []


def test_units_filter_by_rank(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"rank": "Age"})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"aalenian", "bajocian", "bathonian", "callovian"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_filter_by_rank_trims_whitespace(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"rank": " Epoch "})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"early-jurassic", "middle-jurassic", "late-jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_units_filter_by_nonexistent_rank_returns_empty_list(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"rank": "nonexistent-rank"})
    assert response.status_code == 200
    assert response.json() == []


def test_units_filter_by_parent_id(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"parent_id": "mesozoic"})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"triassic", "jurassic", "cretaceous"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_filter_by_nonexistent_parent_id_returns_empty_list(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"parent_id": "nonexistent-parent"})
    assert response.status_code == 200
    assert response.json() == []


def test_filter_by_rank_and_parent_id_with_no_matching_units(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"rank": "Epoch", "parent_id": "mesozoic"})
    assert response.status_code == 200
    assert response.json() == []


def test_filter_by_rank_and_parent_id_returns_matching_units(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"rank": "Epoch", "parent_id": "jurassic"})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"early-jurassic", "middle-jurassic", "late-jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_filter_by_parent_id_trims_whitespace(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"parent_id": " jurassic "})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"early-jurassic", "middle-jurassic", "late-jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_units_filter_by_at_time(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"at_time": 165.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"mesozoic", "jurassic", "middle-jurassic", "callovian"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


@pytest.mark.parametrize("parameter", [
    "min_age_ma",
    "max_age_ma"
])
def test_at_time_conflicts_with_age_range_filters(client, mesozoic_unit, parameter):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"at_time": 165.0, parameter: 160.0})

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot combine at_time with min_age_ma/max_age_ma"


def test_at_time_on_exact_boundary(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"at_time": 165.3})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"mesozoic", "jurassic", "middle-jurassic", "callovian"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_units_filter_by_min_age_ma(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"min_age_ma": 166.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"triassic", "early-jurassic", "aalenian", "bajocian"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_min_age_ma_filter_includes_exact_boundary(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"min_age_ma": 174.7})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"triassic", "early-jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_units_filter_by_max_age_ma(client, mesozoic_unit, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"max_age_ma": 170.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"bathonian", "callovian", "late-jurassic", "cretaceous", "pleistocene"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_max_age_ma_filter_includes_exact_boundary(client, mesozoic_unit, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"max_age_ma": 161.5})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"late-jurassic", "cretaceous", "pleistocene"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_filter_by_valid_age_range(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/",
                          params={"min_age_ma": 160.0, "max_age_ma": 170.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"bathonian", "callovian"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_filter_units_by_invalid_time_range(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/",
                          params={"min_age_ma": 170.0, "max_age_ma": 160.0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid range: 'min_age_ma' must be less than 'max_age_ma'"


def test_age_range_older_than_all_units_returns_empty_list(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/", params={"min_age_ma": 255.0, "max_age_ma": 300.0})
    assert response.status_code == 200
    assert response.json() == []


def test_equal_min_and_max_age_returns_400(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/",
                          params={"min_age_ma": 150.0, "max_age_ma": 150.0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid range: 'min_age_ma' must be less than 'max_age_ma'"


def test_rank_with_age_range_filters(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/",
                          params={"rank": "Period", "min_age_ma": 140.0, "max_age_ma": 210.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_parent_id_with_age_range_filters(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/",
                          params={"parent_id": "mesozoic", "min_age_ma": 65.0, "max_age_ma": 202.0})
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"jurassic", "cretaceous"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


@pytest.mark.parametrize("parameter", [
    "at_time",
    "min_age_ma",
    "max_age_ma"
])
def test_units_filter_by_invalid_value_should_fail(client, mesozoic_unit, parameter):
    response = client.get("/geologic-time-scale-api/v1/units/",
                     params={parameter: "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", parameter]


def test_get_pleistocene_epoch(client, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/pleistocene")
    assert response.status_code == 200

    unit = response.json()

    assert_unit_has_required_properties(unit)
    assert_unit_matches_expected_values(unit, **EXPECTED_UNITS["pleistocene"])


def test_get_nonexistent_unit(client, mesozoic_unit, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_get_jurassic_parent_as_mesozoic(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/jurassic/parent_unit")
    assert response.status_code == 200

    unit = response.json()
    assert_unit_has_required_properties(unit)
    assert_unit_matches_expected_values(unit, **EXPECTED_UNITS["mesozoic"])


def test_get_parent_of_root_unit_returns_404(client, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/pleistocene/parent_unit")
    assert response.status_code == 404
    assert response.json()["detail"] == "Parent unit not found"


def test_get_parent_of_nonexistent_unit_returns_404(client):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent/parent_unit")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_get_jurassic_children(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/jurassic/child_units")
    assert response.status_code == 200

    units = response.json()
    expected_ids = {"early-jurassic", "middle-jurassic", "late-jurassic"}
    assert_units_match_expected(units, expected_ids, EXPECTED_UNITS)


def test_get_children_from_nonexistent_unit_should_fail(client):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent/child_units")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_get_children_of_leaf_unit_returns_empty_list(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/callovian/child_units")
    assert response.status_code == 200
    assert response.json() == []


def test_get_jurassic_duration(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/jurassic/duration")
    assert response.status_code == 200

    unit_duration = response.json()
    assert isinstance(unit_duration, dict)
    assert unit_duration.get("duration_ma") == pytest.approx(58.300)
    assert unit_duration.get("formatted_duration") == "58.300 Ma"


def test_get_duration_of_nonexistent_unit(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent_unit/duration")
    assert response.status_code == 404


def test_get_pleistocene_description(client, pleistocene_unit):
    response = client.get("/geologic-time-scale-api/v1/units/pleistocene/description")
    assert response.status_code == 200

    unit_description = response.json()
    assert isinstance(unit_description, dict)
    assert unit_description.get("description") == "Pleistocene - Epoch lasted from 2.58 Ma to 11.7 ka"


def test_get_description_of_nonexistent_unit_returns_404(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent/description")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_get_callovian_path(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/callovian/path")
    assert response.status_code == 200

    unit_path = response.json()
    assert isinstance(unit_path, dict)
    assert unit_path["path"] == ["Mesozoic", "Jurassic", "Middle Jurassic", "Callovian"]


def test_get_nonexistent_unit_path_should_fail(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/nonexistent/path")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_get_root_unit_path(client, mesozoic_unit):
    response = client.get("/geologic-time-scale-api/v1/units/mesozoic/path")
    assert response.status_code == 200

    unit_path = response.json()
    assert isinstance(unit_path, dict)
    assert unit_path["path"] == ["Mesozoic"]


def test_get_unit_path_with_parent_cycle_returns_409(client, mesozoic_unit, test_db_session):
    mesozoic = test_db_session.query(
        ChronostratigraphicUnitDB).filter_by(id="mesozoic").one()
    mesozoic.parent_id = "callovian"
    test_db_session.commit()

    response = client.get("/geologic-time-scale-api/v1/units/callovian/path")
    assert response.status_code == 409
    assert response.json()["detail"] == "Parent hierarchy contains a cycle"
