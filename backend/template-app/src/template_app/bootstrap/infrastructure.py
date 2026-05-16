from __future__ import annotations

from template_app.infrastructure.providers.database import DatabaseProvider
from template_app.infrastructure.providers.redis import RedisProvider
from template_app.infrastructure.providers.registry import (
    InfrastructureRegistry,
)


def bootstrap_infrastructure() -> InfrastructureRegistry:
    """Bootstrap infrastructure providers."""

    registry = InfrastructureRegistry()

    registry.register(DatabaseProvider())
    registry.register(RedisProvider())

    return registry
