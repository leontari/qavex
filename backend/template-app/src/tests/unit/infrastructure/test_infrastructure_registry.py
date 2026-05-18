from __future__ import annotations

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.infrastructure.cache.provider import (
    CacheProvider,
)


def test_registry_registers_provider() -> None:
    registry = InfrastructureRegistry()

    provider = CacheProvider(
        url="redis://localhost",
    )

    registry.register(provider)

    resolved = registry.get("cache")

    assert resolved is provider
