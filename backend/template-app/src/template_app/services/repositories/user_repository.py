"""
SQLAlchemy repository for user persistence operations.

This module defines the UserRepository class, which encapsulates all
database interactions for user entities using SQLAlchemy's async ORM.
"""

from __future__ import annotations

from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from template_app.models.user import User, UserCreate, UserUpdate
from template_app.models.user_orm import UserORM


class UserRepository:
    """Repository class for managing user persistence using SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session (AsyncSession): Active SQLAlchemy async session.
        """
        self.session = session

    async def list(self) -> List[User]:
        """Return all stored users."""
        result = await self.session.execute(select(UserORM))
        rows = result.scalars().all()
        return [User.model_validate(row) for row in rows]

    async def get(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        row = result.scalar_one_or_none()
        return User.model_validate(row) if row else None

    async def create(self, data: UserCreate) -> User:
        """Create and store a new user."""
        obj = UserORM(
            email=data.email,
            full_name=data.full_name,
            is_active=True,
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return User.model_validate(obj)

    async def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        """Update an existing user."""
        values = data.model_dump(exclude_unset=True)
        if not values:
            return None

        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        obj = result.scalar_one_or_none()
        if not obj:
            return None

        for key, value in values.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return User.model_validate(obj)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID."""
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        obj = result.scalar_one_or_none()
        if not obj:
            return False

        await self.session.delete(obj)
        await self.session.commit()
        return True
