"""
Mail runtime settings.

This module contains environment-driven email delivery configuration
used by the application's notification and messaging subsystem.

The settings defined here control:
- SMTP connectivity
- mail transport security
- sender identity
- authentication credentials
- TLS/SSL behavior

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes secrets
- CI/CD runtime injection

Typical use cases:
- transactional emails
- password reset emails
- account verification
- system notifications
- background mail delivery

Security considerations:
    SMTP credentials should never be hardcoded in production.

    Production deployments should:
    - use secret stores
    - enable TLS encryption
    - avoid plaintext credentials in repositories
    - isolate mail infrastructure access

Example:
    MAIL_HOST=smtp.example.com
    MAIL_PORT=587
    MAIL_USERNAME=mailer
    MAIL_PASSWORD=super-secret-password

Design principles:
    - strict typing
    - immutable runtime configuration
    - deployment portability
    - secure credential handling
"""

from __future__ import annotations

from pydantic import (
    EmailStr,
    SecretStr,
)
from pydantic_settings import BaseSettings

from template_app.config_.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class MailSettings(BaseSettings):
    """
    Runtime mail delivery configuration.

    This settings model defines SMTP connectivity and email delivery
    runtime behavior.

    Attributes:
        MAIL_ENABLED:
            Enables outbound email delivery.

        MAIL_HOST:
            SMTP server hostname.

        MAIL_PORT:
            SMTP server port.

        MAIL_USERNAME:
            SMTP authentication username.

        MAIL_PASSWORD:
            SMTP authentication password.

        MAIL_FROM:
            Default sender email address.

        MAIL_USE_TLS:
            Enables STARTTLS transport encryption.

        MAIL_USE_SSL:
            Enables SSL/TLS encrypted SMTP connections.
    """

    MAIL_ENABLED: bool = False

    MAIL_HOST: str = "localhost"

    MAIL_PORT: int = 1025

    MAIL_USERNAME: str | None = None

    MAIL_PASSWORD: SecretStr | None = None

    MAIL_FROM: EmailStr = "noreply@example.com"

    MAIL_USE_TLS: bool = True

    MAIL_USE_SSL: bool = False

    model_config = COMMON_SETTINGS_CONFIG
