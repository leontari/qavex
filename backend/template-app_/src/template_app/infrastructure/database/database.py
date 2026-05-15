"""
Database configuration for the Template App service.

This module defines:
  * async SQLAlchemy engine
  * session factory
  * FastAPI dependency for obtaining DB sessions

The configuration is environment‑driven and fully compatible with:
  * wheel installation
  * Docker deployment
  * local development
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from template_app.config_.settings import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# Create engine from environment-driven settings
engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
)


# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    """
    FastAPI dependency that provides a database session.

    Yields:
        AsyncSession: Active SQLAlchemy async session.

    """
    async with AsyncSessionLocal() as session:
        yield session
