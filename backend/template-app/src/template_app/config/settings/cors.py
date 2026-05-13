"""
CORS runtime settings.

This module contains environment-driven Cross-Origin Resource Sharing
(CORS) configuration used by the web application.

The settings defined here control browser cross-origin access policies
for HTTP APIs and web clients.

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes runtime environments
- CI/CD secret injection

These settings are typically used by:
- FastAPI CORSMiddleware
- API gateways
- reverse proxies
- browser-based frontend applications

Security considerations:
    Production environments should avoid wildcard origins ("*")
    whenever credentials or authentication headers are enabled.

    Prefer explicit trusted origins in production deployments.

Example:
    CORS_ALLOW_ORIGINS=["https://example.com"]

Design principles:
    - strict typing
    - environment isolation
    - secure production defaults
    - deployment portability

"""

from __future__ import annotations

from pydantic_settings import BaseSettings

from template_app.config.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class CORSSettings(BaseSettings):
    """
    Runtime CORS configuration.

    This settings model defines browser cross-origin access policies
    for the application API.

    Attributes:
        CORS_ALLOW_ORIGINS:
            List of allowed cross-origin domains.

        CORS_ALLOW_CREDENTIALS:
            Enables cookies and authorization headers in cross-origin
            requests.

        CORS_ALLOW_METHODS:
            List of allowed HTTP methods for cross-origin requests.

        CORS_ALLOW_HEADERS:
            List of allowed HTTP headers for cross-origin requests.
    """

    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    CORS_ALLOW_METHODS: list[str] = ["*"]

    CORS_ALLOW_HEADERS: list[str] = ["*"]

    model_config = COMMON_SETTINGS_CONFIG
