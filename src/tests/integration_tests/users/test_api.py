import pytest


@pytest.mark.parametrize("email, password", [("user@example.com", "string")])
async def test_full_flow_auth(
    email,
    password,
    ac,
):
    response_register = await ac.post("/auth/register", json={"email": email, "password": password})

    assert response_register.status_code == 200
    assert response_register.json()["status"] == "Ok"

    response_login = await ac.post("/auth/login", json={"email": email, "password": password})

    assert response_login.status_code == 200
    assert ac.cookies.get("access_token")

    response_me = await ac.get("/auth/me")

    assert response_me.status_code == 200
    assert isinstance(response_me.json(), dict)
    assert isinstance(response_me.json()["id"], int)

    await ac.post("/auth/logout")
    assert response_login.status_code == 200

    response_me2 = await ac.get("/auth/me")
    assert response_me2.json()["detail"]
