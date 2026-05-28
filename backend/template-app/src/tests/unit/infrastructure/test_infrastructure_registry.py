from __future__ import annotations

from template_app.runtime.infrastructure import (
    InfrastructureRegistry,
)
from template_app.runtime.infrastructure import (
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
