"""
User domain models.

This module defines Pydantic models used for representing user data
across API requests and responses. These models are shared between
routers and service-layer components.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    """Represents a user returned by the API.

    Attributes:
        id (int): Unique identifier of the user.
        email (EmailStr): Email address of the user.
        full_name (str | None): Optional full name of the user.
        is_active (bool): Indicates whether the user account is active.
    """

    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Payload for creating a new user.

    Attributes:
        email (EmailStr): Email address for the new user.
        password (str): Raw password provided during registration.
        full_name (str | None): Optional full name of the user.
    """

    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(BaseModel):
    """Payload for updating an existing user.

    Attributes:
        email (EmailStr | None): Updated email address.
        full_name (str | None): Updated full name.
        is_active (bool | None): Updated active status.
    """

    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None
