from __future__ import annotations

from template_app.infrastructure.cache.provider import (
    CacheProvider,
)
from template_app.infrastructure.database.provider import (
    DatabaseProvider,
)
from template_app.infrastructure.queue.provider import (
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
