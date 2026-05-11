import pytest
from template_app.services.auth_service import AuthService
from template_app.services.repositories.user_repository import UserRepository
from template_app.models.user import UserCreate


@pytest.mark.asyncio
async def test_register_user(session):
    service = AuthService(UserRepository(session))

    user = await service.register_user(
        UserCreate(email="auth@test.com", password="pass")
    )

    assert user.email == "auth@test.com"


@pytest.mark.asyncio
async def test_login_success(session):
    service = AuthService(UserRepository(session))

    await service.register_user(UserCreate(email="a@b.com", password="x"))

    tokens = await service.login("a@b.com", "x")

    assert "access_token" in tokens
