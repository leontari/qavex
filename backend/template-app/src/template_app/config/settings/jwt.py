"""
JWT runtime settings.

This module contains environment-driven JSON Web Token (JWT)
configuration used for authentication and authorization.

The settings defined here control:
- token signing
- token verification
- cryptographic algorithms
- token expiration policies

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes secrets
- CI/CD secret injection

Security considerations:
    JWT secrets must never be hardcoded in production.

    Production deployments should inject JWT_SECRET_KEY via:
    - Kubernetes secrets
    - Docker secrets
    - cloud secret managers
    - CI/CD secret stores

    Weak or default secret values must never be used in production.

Supported algorithms:
    - HS256
    - HS384
    - HS512
    - RS256
    - ES256
    - other PyJWT-supported algorithms

Example:
    JWT_SECRET_KEY=super-secure-random-secret

Design principles:
    - strict typing
    - immutable runtime configuration
    - production security
    - deployment portability

"""

from __future__ import annotations

from pydantic import (
    Field,
    SecretStr,
)
from pydantic_settings import BaseSettings

from template_app.config.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class JWTSettings(BaseSettings):
    """
    Runtime JWT authentication configuration.

    This settings model defines cryptographic and expiration settings
    used for JWT-based authentication and authorization.

    Attributes:
        JWT_SECRET_KEY:
            Secret key used for JWT signing and verification.

        JWT_ALGORITHM:
            Cryptographic algorithm used for JWT encoding.

        JWT_ACCESS_TOKEN_EXPIRE_MINUTES:
            Access token lifetime in minutes.

    """

    JWT_SECRET_KEY: SecretStr = Field(
        default=SecretStr("CHANGE_ME"),
    )

    JWT_ALGORITHM: str = "HS256"

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = COMMON_SETTINGS_CONFIG
