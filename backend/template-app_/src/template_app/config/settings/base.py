"""
Base application settings.

This module contains core runtime configuration shared across all
application environments.

The settings defined here are environment-driven and loaded via
Pydantic Settings from:
- environment variables
- .env files
- Docker/Kubernetes runtime environments

This module should contain only generic application-level settings,
such as:
- environment mode
- debug flag
- logging level
- API behavior

Infrastructure-specific settings (database, redis, jwt, etc.)
must be defined in dedicated modules.
"""

from __future__ import annotations

from pydantic import computed_field
from pydantic_settings import BaseSettings

from template_app.config_.enums import Environment, LogLevel
from template_app.config_.settings.common import COMMON_SETTINGS_CONFIG


class BaseAppSettings(BaseSettings):
    """
    Base runtime application settings.

    This class defines shared application-level runtime configuration
    loaded from environment variables.

    Attributes:
        APP_ENV:
            Current application environment.

        DEBUG:
            Enables debug mode.

        LOG_LEVEL:
            Application logging level.

    """

    APP_ENV: Environment = Environment.LOCAL

    DEBUG: bool = False

    LOG_LEVEL: LogLevel = LogLevel.INFO

    model_config = COMMON_SETTINGS_CONFIG

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_production(self) -> bool:
        """
        Determine whether the application runs in production mode.

        Returns:
            bool:
                True if APP_ENV equals PROD,
                otherwise False.

        """
        return self.APP_ENV == Environment.PROD

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_development(self) -> bool:
        """
        Determine whether the application runs in local development mode.

        Returns:
            bool:
                True if APP_ENV equals LOCAL,
                otherwise False.

        """
        return self.APP_ENV == Environment.LOCAL

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_testing(self) -> bool:
        """
        Determine whether the application runs in testing mode.

        Returns:
            bool:
                True if APP_ENV equals TEST or CI,
                otherwise False.

        """
        return self.APP_ENV in {
            Environment.TEST,
            Environment.CI,
        }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_docker(self) -> bool:
        """
        Determine whether the application runs inside Docker.

        Returns:
            bool:
                True if APP_ENV equals DOCKER,
                otherwise False.

        """
        return self.APP_ENV == Environment.DOCKER
