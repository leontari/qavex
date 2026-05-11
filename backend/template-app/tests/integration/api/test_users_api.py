import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users/", json={"email": "int@test.com", "password": "123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "int@test.com"
