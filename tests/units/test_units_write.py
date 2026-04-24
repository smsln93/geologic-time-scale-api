from typing import Any, Dict

from tests.utils.assertions import assert_unit, assert_unit_has_required_properties


def test_create_triassic_unit_valid_api_key(client, valid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "triassic",
        "name": "Triassic",
        "rank": "Period",
        "begin_time_ma": 251.902,
        "begin_uncertainty_ma": 0.024,
        "end_time_ma": 201.4,
        "end_uncertainty_ma": 0.2,
        "parent_id": "mesozoic"
    }

    res = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert res.status_code == 201

    new_unit = res.json()
    assert_unit(new_unit,
                expected_id=payload["id"],
                expected_name=payload["name"],
                expected_rank=payload["rank"],
                expected_rank_order=4,  # Period -> 4
                expected_begin_time_ma=payload["begin_time_ma"],
                expected_begin_uncertainty_ma=payload["begin_uncertainty_ma"],
                expected_end_time_ma=payload["end_time_ma"],
                expected_end_uncertainty_ma=payload["end_uncertainty_ma"],
                expected_parent_id=payload["parent_id"])


def test_create_triassic_unit_invalid_api_key(client, invalid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "triassic",
        "name": "Triassic",
        "rank": "Period",
        "begin_time_ma": 251.902,
        "begin_uncertainty_ma": 0.024,
        "end_time_ma": 201.4,
        "end_uncertainty_ma": 0.2,
        "parent_id": "mesozoic"
    }

    res = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=invalid_authentication_header)
    assert res.status_code == 403


def test_create_jurassic_unit_duplicate_id(client, valid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "jurassic",
        "name": "Jurassic",
        "rank": "Period",
        "begin_time_ma": 201.4,
        "begin_uncertainty_ma": 0.2,
        "end_time_ma": 143.1,
        "end_uncertainty_ma": 0.6,
        "parent_id": "mesozoic"
    }

    res = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert res.status_code == 409


def test_create_triassic_unit_invalid_payload(client, valid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "triassic",
        "name": "Triassic",
        "begin_time_ma": 251.902,
        "begin_uncertainty_ma": 0.024,
        "end_time_ma": 201.4,
        "end_uncertainty_ma": 0.2,
        "parent_id": "mesozoic"
    }

    res = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert res.status_code == 422


def test_create_triassic_unit_parent_not_exist(client, valid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "triassic",
        "name": "Triassic",
        "rank": "Period",
        "begin_time_ma": 251.902,
        "begin_uncertainty_ma": 0.024,
        "end_time_ma": 201.4,
        "end_uncertainty_ma": 0.2,
        "parent_id": "non-existent-parent"
    }

    res = client.post("/geologic-time-scale-api/v1/units/", json=payload, headers=valid_authentication_header)
    assert res.status_code == 422


def test_update_mesosoic_unit(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "id": "mesozoic",
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
    if unit.get("id") == "mesozoic":
        assert_unit(unit,
                    expected_id="mesozoic",
                    expected_name="Updated Mesozoic",
                    expected_rank="Era",
                    expected_rank_order=3,
                    expected_begin_time_ma=248.7,
                    expected_begin_uncertainty_ma=2.1,
                    expected_end_time_ma=65.5,
                    expected_end_uncertainty_ma=0.8,
                    expected_parent_id=None)


def test_update_triassic_unit_not_found(client, valid_authentication_header, mesozoic_unit):
    payload: Dict[str, Any] = {
        "id": "triassic",
        "name": "Updated Triassic",
        "rank": "Epoch",
        "begin_time_ma": 248.3,
        "begin_uncertainty_ma": 0.4,
        "end_time_ma": 199.9,
        "end_uncertainty_ma": 1.6,
        "parent_id": "mesozoic"
    }

    res = client.put("/geologic-time-scale-api/v1/units/triassic", json=payload, headers=valid_authentication_header)
    assert res.status_code == 404


def test_update_mesosoic_unit_name(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "name": "Patched Mesozoic"
    }

    res = client.patch("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert res.status_code == 200

    unit = res.json()
    assert isinstance(unit, dict)
    assert_unit_has_required_properties(unit)

    if unit.get("id") == "mesozoic":
        assert_unit(unit,
                    expected_id="mesozoic",
                    expected_name="Patched Mesozoic",
                    expected_rank="Era",
                    expected_rank_order=3,
                    expected_begin_time_ma=251.902,
                    expected_begin_uncertainty_ma=0.024,
                    expected_end_time_ma=66.0,
                    expected_end_uncertainty_ma=0.0,
                    expected_parent_id=None)


def test_update_mesozoic_unit_invalid_field(client, valid_authentication_header, mesozoic_unit):
    payload = {
        "unknown_field": "TEST"
    }

    res = client.patch("/geologic-time-scale-api/v1/units/mesozoic", json=payload, headers=valid_authentication_header)
    assert res.status_code == 422


def test_delete_callovian_unit(client, valid_authentication_header, mesozoic_unit):
    res = client.delete("/geologic-time-scale-api/v1/units/callovian", headers=valid_authentication_header)
    assert res.status_code == 204


def test_delete_unit_not_found(client, valid_authentication_header, mesozoic_unit):
    res = client.delete("/geologic-time-scale-api/v1/units/non-existent", headers=valid_authentication_header)
    assert res.status_code == 404


def test_delete_protects_parent_unit(client, valid_authentication_header, mesozoic_unit):
    res = client.delete("/geologic-time-scale-api/v1/units/jurassic", headers=valid_authentication_header)
    assert res.status_code == 400
