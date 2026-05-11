import pytest
from template_app.services.user_service import UserService
from template_app.services.repositories.user_repository import UserRepository
from template_app.models.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_user(session):
    service = UserService(UserRepository(session))

    user = await service.create_user(
        UserCreate(email="u@test.com", password="123", full_name="User")
    )

    assert user.id is not None
    assert user.email == "u@test.com"


@pytest.mark.asyncio
async def test_update_user(session):
    service = UserService(UserRepository(session))

    created = await service.create_user(
        UserCreate(email="old@test.com", password="123")
    )

    updated = await service.update_user(
        created.id, UserUpdate(full_name="New Name")
    )

    assert updated.full_name == "New Name"
