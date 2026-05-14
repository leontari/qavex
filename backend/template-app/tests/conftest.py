from __future__ import annotations

import asyncio
import logging

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from template_app.core_.app_.factory import create_app
from template_app.core_.database import get_session
from template_app.core_.dependencies import (
    get_user_repository,
    get_user_service,
)
from template_app.services.repositories.user_repository import UserRepository
from template_app.services.user_service import UserService
from template_app.models_.sqlalchemy_base import Base


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncSession:
    async_session = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


@pytest.fixture
def app(test_session):
    app = create_app()

    async def override_get_session():
        yield test_session

    def override_user_repo():
        return UserRepository(test_session)

    def override_user_service():
        return UserService(UserRepository(test_session))

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_user_repository] = override_user_repo
    app.dependency_overrides[get_user_service] = override_user_service

    return app


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def caplog_info(caplog):
    with caplog.at_level(logging.INFO):
        yield caplog





from template_app.bootstrap.testing import (
    bootstrap_testing_application,
)

@pytest.fixture
def app():
    context = bootstrap_testing_application()

    return context.app
