from __future__ import annotations

from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.infrastructure.cache.provider import (
    CacheProvider,
)
from template_app.infrastructure.database.provider import (
    DatabaseProvider,
)
from template_app.infrastructure.queue.provider import (
    QueueProvider,
)


def build_infrastructure_registry() -> InfrastructureRegistry:
    """Build infrastructure registry."""

    registry = InfrastructureRegistry()

    registry.register(
        CacheProvider(
            url="redis://localhost:6379",
        ),
    )

    registry.register(
        DatabaseProvider(
            dsn="postgresql://localhost/test",
        ),
    )

    registry.register(
        QueueProvider(
            brokers=["localhost:9092"],
        ),
    )

    return registry
