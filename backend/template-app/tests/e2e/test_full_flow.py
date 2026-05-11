import pytest


@pytest.mark.asyncio
async def test_full_flow(client):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"email": "flow@test.com", "password": "pass"},
    )

    # Login
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": "flow@test.com", "password": "pass"},
    )
    token = login.json()["access_token"]

    # Create user via API
    response = await client.post(
        "/api/v1/users/",
        json={"email": "flow2@test.com", "password": "pass"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
