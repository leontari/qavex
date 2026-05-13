from __future__ import annotations

from enum import StrEnum


class AppEnv(StrEnum):
    """Application environment."""

    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class LogFormat(StrEnum):
    """Supported log formats."""

    JSON = "json"
    CONSOLE = "console"
