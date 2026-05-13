"""
SQLAlchemy declarative base for ORM models.

This module defines the shared Base class used by all SQLAlchemy ORM
models in the Template App service.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={getattr(self, 'id', None)!r}>"
