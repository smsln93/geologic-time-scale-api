from typing import Any

from tests.utils.assertions import assert_unit_matches_expected_values, assert_unit_has_required_properties
from tests.utils.expected_units import EXPECTED_UNITS


def test_create_unit_returns_201(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "cretaceous"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert response.status_code == 201

    new_unit = response.json()
    assert_unit_matches_expected_values(new_unit,
                                        expected_id=payload["id"],
                                        expected_name=payload["name"],
                                        expected_rank=payload["rank"],
                                        expected_rank_order=5,
                                        expected_begin_time_ma=payload["begin_time_ma"],
                                        expected_begin_uncertainty_ma=payload["begin_uncertainty_ma"],
                                        expected_end_time_ma=payload["end_time_ma"],
                                        expected_end_uncertainty_ma=payload["end_uncertainty_ma"],
                                        expected_parent_id=payload["parent_id"])


def test_create_unit_with_duplicate_id_returns_409(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "jurassic",
        "name": "Jurassic",
        "rank": "Period",
        "begin_time_ma": 201.4,
        "begin_uncertainty_ma": 0.2,
        "end_time_ma": 143.1,
        "end_uncertainty_ma": 0.6,
        "parent_id": "mesozoic"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert response.status_code == 409
    assert response.json()["detail"] == "Unit already exists"


def test_create_unit_with_invalid_api_key(client, invalid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "cretaceous"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=invalid_authentication_header)
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API Key"


def test_create_unit_without_api_key(client, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "cretaceous"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "API key is missing"


def test_create_unit_without_rank_returns_422(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "cretaceous"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert response.status_code == 422
    assert any(error["loc"] == ["body", "rank"] for error in response.json()["detail"])


def test_create_unit_with_nonexistent_parent(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "nonexistent-parent"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert response.status_code == 422
    assert response.json()["detail"] == "Parent unit does not exist"


def test_create_unit_as_its_own_parent(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "id": "late-cretaceous",
        "name": "Late Cretaceous",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "late-cretaceous"
    }

    response = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert response.status_code == 422
    assert any(error["loc"] == ["body"]
               and error["type"] == "value_error"
               and "Unit cannot be its own parent" in error["msg"]
               for error in response.json()["detail"])


def test_replace_unit_data(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "name": "Updated Mesozoic",
        "rank": "Era",
        "begin_time_ma": 248.7,
        "begin_uncertainty_ma": 2.1,
        "end_time_ma": 65.5,
        "end_uncertainty_ma": 0.8,
        "parent_id": None
    }

    res = client.put("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert res.status_code == 200

    unit = res.json()
    assert isinstance(unit, dict)

    assert_unit_has_required_properties(unit)
    assert_unit_matches_expected_values(unit,
                                        expected_id="mesozoic",
                                        expected_name="Updated Mesozoic",
                                        expected_rank="Era",
                                        expected_rank_order=3,
                                        expected_begin_time_ma=248.7,
                                        expected_begin_uncertainty_ma=2.1,
                                        expected_end_time_ma=65.5,
                                        expected_end_uncertainty_ma=0.8,
                                        expected_parent_id=None)


def test_replace_unit_with_parent_cycle_returns_422(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "name": "Updated Mesozoic",
        "rank": "Era",
        "begin_time_ma": 248.7,
        "begin_uncertainty_ma": 2.1,
        "end_time_ma": 65.5,
        "end_uncertainty_ma": 0.8,
        "parent_id": "callovian"
    }

    res = client.put("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert res.status_code == 422
    assert res.json()["detail"] == "Circular parent relationship"


def test_replace_nonexistent_unit_returns_404(client, valid_authentication_header, mesozoic_unit):
    payload: dict[str, Any] = {
        "name": "Nonexistent Unit",
        "rank": "Epoch",
        "begin_time_ma": 100.5,
        "begin_uncertainty_ma": 0.1,
        "end_time_ma": 66.0,
        "end_uncertainty_ma": 0.0,
        "parent_id": "cretaceous"
    }

    response = client.put("/geologic-time-scale-api/v1/units/nonexistent-unit", json=payload, headers=valid_authentication_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_update_unit_name(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "name": "Patched Mesozoic"
    }

    response = client.patch("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert response.status_code == 200

    unit = response.json()
    assert_unit_has_required_properties(unit)

    expected = EXPECTED_UNITS["mesozoic"].copy()
    expected["expected_name"] = "Patched Mesozoic"

    assert_unit_matches_expected_values(unit, **expected)


def test_update_unit_invalid_field(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "unknown_field": "TEST"
    }

    response = client.patch("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert response.status_code == 422

    assert any(
        error["loc"] == ["body", "unknown_field"]
        and error["type"] == "extra_forbidden"
        for error in response.json()["detail"]
    )


def test_update_nonexistent_unit(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "name": "TEST"
    }

    response = client.patch("/geologic-time-scale-api/v1/units/nonexistent-unit", json=payload, headers=valid_authentication_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_update_unit_parent_id_to_create_cycle(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "parent_id": "callovian"
    }

    response = client.patch("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert response.status_code == 422
    assert response.json()["detail"] == "Circular parent relationship"


def test_update_unit_rank(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "rank": "Epoch"
    }

    res = client.patch("/geologic-time-scale-api/v1/units/callovian", json=payload, headers=valid_authentication_header)
    assert res.status_code == 200

    unit = res.json()
    assert_unit_has_required_properties(unit)

    expected = EXPECTED_UNITS["callovian"].copy()
    expected["expected_rank"] = "Epoch"
    expected["expected_rank_order"] = 5

    assert_unit_matches_expected_values(unit, **expected)


def test_delete_unit(client, valid_authentication_header, mesozoic_unit):
    response = client.delete("/geologic-time-scale-api/v1/units/callovian", headers=valid_authentication_header)
    assert response.status_code == 204

    get_response = client.get("/geologic-time-scale-api/v1/units/callovian")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Unit not found"}


def test_delete_unit_not_found(client, valid_authentication_header, mesozoic_unit):
    response = client.delete("/geologic-time-scale-api/v1/units/non-existent", headers=valid_authentication_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Unit not found"


def test_delete_unit_with_children_returns_400(client, valid_authentication_header, mesozoic_unit):
    res = client.delete("/geologic-time-scale-api/v1/units/jurassic", headers=valid_authentication_header)
    assert res.status_code == 400
    assert res.json()["detail"] == "Cannot delete unit with child units"
