

import json


async def test_add_facilities(ac):
    response = await ac.post(
        "/facilities",
        params=json.dumps({"title": "dlksflkdjf"})
    )
    print(response.json())
    assert response

async def test_get_facilities(ac):
    facilities = await ac.get(
        "/facilities"
    )
    
    print(facilities.json())
    assert facilities.status_code == 200