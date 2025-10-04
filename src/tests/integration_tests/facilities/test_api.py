async def test_post_facilities(ac):
    facility_title = "Массаж"
    response = await ac.post("/facilities", json={"title": facility_title})
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res["data"]["data"]["title"] == facility_title


async def test_get_facilities(ac):
    facilities = await ac.get("/facilities")

    print(facilities.json())
    assert facilities.status_code == 200
