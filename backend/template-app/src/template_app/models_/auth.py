"""
Authentication and authorization models.

This module defines Pydantic models used for login, token generation,
and authentication-related API responses.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Payload for user login.

    Attributes:
        email (EmailStr): User email address.
        password (str): User password.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Represents an access token returned after successful authentication.

    Attributes:
        access_token (str): JWT or opaque token string.
        token_type (str): Type of the token, typically 'bearer'.
    """

    access_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Payload for refreshing an access token.

    Attributes:
        refresh_token (str): Refresh token issued during login.
    """

    refresh_token: str
