"""
SQLAlchemy ORM model for the User entity.

This module defines the UserORM class, which represents the database
schema for user records. ORM models are used by the repository layer
to interact with the underlying database.
"""

from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from template_app.models.sqlalchemy_base import Base
from template_app.models.mixins import TimestampMixin


class UserORM(TimestampMixin, Base):
    """SQLAlchemy ORM representation of a user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<UserORM id={self.id} email={self.email!r}>"
