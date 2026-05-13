"""
Shared settings utilities.

This module contains shared utilities and base configuration used by
all runtime settings modules.

Responsibilities:
- runtime environment detection
- .env file resolution
- shared Pydantic settings configuration
- centralized settings behavior

The configuration system supports multiple deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations
- wheel/package installations

Environment resolution:
    The active runtime environment is determined by the APP_ENV
    environment variable.

Supported environments:
    - local
    - test
    - ci
    - docker
    - prod

Environment file mapping:
    APP_ENV=local   -> .env.local
    APP_ENV=test    -> .env.test
    APP_ENV=ci      -> .env.ci
    APP_ENV=docker  -> .env.docker
    APP_ENV=prod    -> .env

Pydantic settings priority:
    1. Environment variables
    2. .env files
    3. Default values

This priority model ensures that:
- Kubernetes secrets override .env values
- Docker runtime variables override local configuration
- CI/CD injected variables override repository defaults

Design principles:
    - deployment portability
    - environment isolation
    - centralized configuration behavior
    - immutable runtime configuration
    - production-safe defaults
"""

from __future__ import annotations

import os

from pydantic_settings import SettingsConfigDict

# ============================================================================
# Runtime environment detection
# ============================================================================

APP_ENV: str = os.getenv("APP_ENV", "local")

# ============================================================================
# Environment file mapping
# ============================================================================

ENV_FILES: dict[str, str] = {
    "local": ".env.local",
    "test": ".env.test",
    "ci": ".env.ci",
    "docker": ".env.docker",
    "prod": ".env",
}

# ============================================================================
# Active environment file
# ============================================================================

ENV_FILE: str = ENV_FILES.get(APP_ENV, ".env")

# ============================================================================
# Shared Pydantic settings configuration
# ============================================================================

COMMON_SETTINGS_CONFIG: SettingsConfigDict = SettingsConfigDict(
    env_file=ENV_FILE,
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
    frozen=True,
)
