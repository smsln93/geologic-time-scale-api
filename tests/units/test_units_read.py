def test_get_pleistocene_epoch(client, pleistocene_unit):
    res = client.get("/geologic-time-scale-api/v1/units/pleistocene")

    print(res.json())

    assert res.status_code == 200

    data = res.json()

    assert isinstance(data, dict)

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

    assert expected_keys.issubset(set(data.keys()))

    assert data["id"] == "pleistocene"
    assert data["name"] == "Pleistocene"
    assert data["rank"] == "Epoch"
    assert data["rank_order"] == 5
    assert abs(data["begin_time_ma"] - 2.58) < 1e-6
    assert data["begin_uncertainty_ma"] == 0.0
    assert abs(data["end_time_ma"] - 0.0117) < 1e-6
    assert data["end_uncertainty_ma"] == 0.0
    assert data["parent_id"] is None
