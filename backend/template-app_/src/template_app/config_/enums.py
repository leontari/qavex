"""
Application configuration enums.

This module contains strongly-typed enumerations used throughout the
application configuration system.

The enums defined here provide:
- strict configuration validation
- IDE autocompletion support
- type-safe runtime configuration
- centralized configuration constants
- deployment-safe environment definitions

These enums are primarily used by:
- Pydantic settings models
- logging configuration
- runtime environment detection
- infrastructure configuration
- application bootstrap logic

Design principles:
    - strict typing
    - immutable values
    - centralized configuration constants
    - runtime validation safety
    - deployment portability
"""

from __future__ import annotations

from enum import StrEnum


class Environment(StrEnum):
    """
    Supported application runtime environments.

    This enum defines all officially supported deployment
    and execution environments for the application.

    The environment value controls:
    - environment-specific .env loading
    - runtime behavior
    - logging configuration
    - debugging features
    - infrastructure integration

    Attributes:
        LOCAL:
            Local development environment.

        TEST:
            Automated testing environment.

        CI:
            Continuous integration environment.

        DOCKER:
            Docker container runtime environment.

        PROD:
            Production runtime environment.

    """

    LOCAL = "local"

    TEST = "test"

    CI = "ci"

    DOCKER = "docker"

    PROD = "prod"


class LogFormat(StrEnum):
    """
    Supported application log output formats.

    This enum defines structured logging output formats
    available for the application logging subsystem.

    Attributes:
        JSON:
            Structured JSON logging format suitable for:
            - production environments
            - log aggregation systems
            - ELK stack
            - Loki
            - Datadog
            - cloud-native observability systems

        CONSOLE:
            Human-readable console logging format suitable for:
            - local development
            - debugging
            - interactive terminal usage

    """

    JSON = "json"

    CONSOLE = "console"


class LogLevel(StrEnum):
    """
    Supported application logging levels.

    This enum defines available severity levels for
    the application logging subsystem.

    Attributes:
        DEBUG:
            Detailed debugging information intended for development.

        INFO:
            General informational runtime messages.

        WARNING:
            Warning conditions that do not interrupt execution.

        ERROR:
            Runtime errors affecting specific operations.

        CRITICAL:
            Critical failures that may terminate the application.

    """

    DEBUG = "DEBUG"

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"
