import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "auth@test.com", "password": "pass"},
    )

    login = await client.post(
        "/api/v1/auth/login",
        data={"username": "auth@test.com", "password": "pass"},
    )

    assert login.status_code == 200
    assert "access_token" in login.json()
