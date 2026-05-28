from __future__ import annotations

from template_app.runtime.infrastructure import (
    InfrastructureRegistry,
)
from template_app.runtime.infrastructure import (
    CacheProvider,
)
from template_app.runtime.infrastructure import (
    DatabaseProvider,
)
from template_app.runtime.infrastructure import (
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
