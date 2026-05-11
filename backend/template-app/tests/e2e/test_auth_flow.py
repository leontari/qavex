from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    payload = {
        "email": "auth@test.com",
        "password": "secret123",
        "full_name": "Auth User",
    }

    response = await client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "auth@test.com"
    assert "id" in data
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@test.com", "password": "pass123"},
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@test.com", "password": "pass123"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@test.com", "password": "correct"},
    )

    # Wrong password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpass@test.com", "password": "incorrect"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"email": "me@test.com", "password": "pass"},
    )

    # Login
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "me@test.com", "password": "pass"},
    )
    token = login_resp.json()["access_token"]

    # Call /me
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "me@test.com"


@pytest.mark.asyncio
async def test_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"email": "refresh@test.com", "password": "pass"},
    )

    # Login
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "refresh@test.com", "password": "pass"},
    )
    refresh_token = login_resp.json().get("refresh_token")

    if refresh_token is None:
        pytest.skip("Auth system does not implement refresh tokens")

    # Refresh
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
