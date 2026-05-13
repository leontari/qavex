"""
Dependency injection wiring for the Template App service.

This module defines FastAPI dependencies for repositories and services.
All dependencies are constructed per-request to ensure correct session
lifecycle and testability.
"""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from template_app.core.database import get_session
from template_app.services.repositories.user_repository import UserRepository
from template_app.services.user_service import UserService


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    """Provide a UserRepository instance."""
    return UserRepository(session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Provide a UserService instance."""
    return UserService(repo)
