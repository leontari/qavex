import pytest
from template_app.services.repositories.user_repository import UserRepository
from template_app.models.user_orm import UserORM


@pytest.mark.asyncio
async def test_add_user(session):
    repo = UserRepository(session)

    user = UserORM(email="repo@test.com", full_name="Repo User")
    await repo.add(user)

    fetched = await repo.get_by_id(user.id)
    assert fetched.email == "repo@test.com"
