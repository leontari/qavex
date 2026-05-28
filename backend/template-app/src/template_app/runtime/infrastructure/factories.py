from __future__ import annotations

from template_app.runtime.infrastructure.infra import (
    CacheProvider,
    DatabaseProvider,
    QueueProvider,
)
from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)


def bootstrap_infrastructure() -> InfrastructureRegistry:
    """Bootstrap infrastructure providers."""

    registry = InfrastructureRegistry()

    registry.register(
        CacheProvider(
            url="redis://localhost:6379",
        ),
    )

    registry.register(
        DatabaseProvider(
            dsn="postgresql://localhost/app",
        ),
    )

    registry.register(
        QueueProvider(
            brokers=["localhost:9092"],
        ),
    )

    return registry
