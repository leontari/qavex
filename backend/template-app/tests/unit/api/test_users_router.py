"""
Tests for the /users API endpoints.
"""

# юнит‑тесты роутера (с моками сервисов)
from __future__ import annotations

import pytest

from template_app.models.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_api(client):
    response = await client.post(
        "/api/v1/users/",
        json={"email": "api@x.com", "full_name": "API", "password": "x"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "api@x.com"


@pytest.mark.asyncio
async def test_list_users_api(client):
    await client.post(
        "/api/v1/users/",
        json={"email": "list@x.com", "full_name": "List", "password": "x"},
    )
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_api(client):
    created = await client.post(
        "/api/v1/users/",
        json={"email": "get@x.com", "full_name": "Get", "password": "x"},
    )
    user_id = created.json()["id"]

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "get@x.com"


@pytest.mark.asyncio
async def test_update_user_api(client):
    created = await client.post(
        "/api/v1/users/",
        json={"email": "upd@x.com", "full_name": "Old", "password": "x"},
    )
    user_id = created.json()["id"]

    response = await client.put(
        f"/api/v1/users/{user_id}",
        json={"full_name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_user_api(client):
    created = await client.post(
        "/api/v1/users/",
        json={"email": "del@x.com", "full_name": "Del", "password": "x"},
    )
    user_id = created.json()["id"]

    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
