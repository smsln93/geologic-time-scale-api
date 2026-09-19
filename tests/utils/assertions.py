from typing import Any

from pytest import approx


def assert_unit_matches_expected_values(unit: dict[str, Any], expected_id: str, expected_name: str, expected_rank: str, expected_rank_order: int,
                                        expected_begin_time_ma: float, expected_begin_uncertainty_ma: float, expected_end_time_ma: float,
                                        expected_end_uncertainty_ma: float, expected_parent_id: str | None):

    assert unit["id"] == expected_id
    assert unit["name"] == expected_name
    assert unit["rank"] == expected_rank
    assert unit["rank_order"] == expected_rank_order

    assert unit["begin_time_ma"] == approx(expected_begin_time_ma)
    assert unit["begin_uncertainty_ma"] == approx(expected_begin_uncertainty_ma)
    assert unit["end_time_ma"] == approx(expected_end_time_ma)
    assert unit["end_uncertainty_ma"] == approx(expected_end_uncertainty_ma)

    assert unit["parent_id"] == expected_parent_id


def assert_unit_has_required_properties(unit: dict):
    expected_keys = {
        "id",
        "name",
        "rank",
        "rank_order",
        "begin_time_ma",
        "begin_uncertainty_ma",
        "end_time_ma",
        "end_uncertainty_ma",
        "parent_id"
    }

    assert isinstance(unit, dict)

    missing_keys = expected_keys - set(unit.keys())
    assert not missing_keys, f"Missing required properties: {missing_keys}"

    assert isinstance(unit["id"], str)
    assert isinstance(unit["name"], str)
    assert isinstance(unit["rank"], str)

    assert type(unit["rank_order"]) is int

    assert (unit["parent_id"] is None or isinstance(unit["parent_id"], str))

    for field in [unit["begin_time_ma"],
                  unit["begin_uncertainty_ma"],
                  unit["end_time_ma"],
                  unit["end_uncertainty_ma"]]:
        assert type(field) in (int, float), f"{field} should be a numeric, got {type(field).__name__}"


def assert_units_match_expected(units: list, expected_ids: set, expected_units: dict) -> None:
    assert isinstance(units, list)

    for unit in units:
        assert_unit_has_required_properties(unit)

    actual_ids = [unit["id"] for unit in units]

    assert sorted(actual_ids) == sorted(expected_ids)

    for unit in units:
        assert_unit_matches_expected_values(unit, **expected_units[unit["id"]])


def assert_unit_csv_match_expected_values(unit: dict[str, str],
                                          expected_id: str, expected_name: str, expected_rank: str, expected_rank_order: int,
                                          expected_begin_time_ma: float, expected_begin_uncertainty_ma: float, expected_end_time_ma: float,
                                          expected_end_uncertainty_ma: float, expected_parent_id: str | None
                                          ) -> None:
    assert unit["id"] == expected_id
    assert unit["name"] == expected_name
    assert unit["rank"] == expected_rank
    assert int(unit["rank_order"]) == expected_rank_order
    assert float(unit["begin_time_ma"]) == approx(expected_begin_time_ma)
    assert float(unit["begin_uncertainty_ma"]) == approx(expected_begin_uncertainty_ma)
    assert float(unit["end_time_ma"]) == approx(expected_end_time_ma)
    assert float(unit["end_uncertainty_ma"]) == approx(expected_end_uncertainty_ma)
    assert unit["parent_id"] == (expected_parent_id if expected_parent_id is not None else "")
