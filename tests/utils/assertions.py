from typing import Optional, Any, Dict

from pytest import approx


def assert_unit(unit: Any, expected_id: str, expected_name: str, expected_rank: str, expected_rank_order: int,
                expected_begin_time_ma: float, expected_begin_uncertainty_ma: float, expected_end_time_ma: float,
                expected_end_uncertainty_ma: float, expected_parent_id: Optional[str]):

    assert unit["id"] == expected_id
    assert unit["name"] == expected_name
    assert unit["rank"] == expected_rank
    assert unit["rank_order"] == expected_rank_order

    assert unit["begin_time_ma"] == approx(expected_begin_time_ma)
    assert unit["begin_uncertainty_ma"] == approx(expected_begin_uncertainty_ma)
    assert unit["end_time_ma"] == approx(expected_end_time_ma)
    assert unit["end_uncertainty_ma"] == approx(expected_end_uncertainty_ma)

    if expected_parent_id is not None:
        assert unit["parent_id"] == expected_parent_id
    else:
        assert unit["parent_id"] is None


def assert_unit_has_required_properties(unit: Any):
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


def assert_unit_csv(unit: Dict[str, str],
                    expected_id: str, expected_name: str, expected_rank: str, expected_rank_order: int,
                    expected_begin_time_ma: float, expected_begin_uncertainty_ma: float, expected_end_time_ma: float,
                    expected_end_uncertainty_ma: float, expected_parent_id: Optional[str]
                    ) -> None:
    assert unit["id"] == expected_id
    assert unit["name"] == expected_name
    assert unit["rank"] == expected_rank
    assert int(unit["rank_order"]) == expected_rank_order
    assert float(unit["begin_time_ma"]) == approx(expected_begin_time_ma)
    assert float(unit["begin_uncertainty_ma"]) == approx(expected_begin_uncertainty_ma)
    assert float(unit["end_time_ma"]) == approx(expected_end_time_ma)
    assert float(unit["end_uncertainty_ma"]) == approx(expected_end_uncertainty_ma)
    assert unit["parent_id"] == expected_parent_id
