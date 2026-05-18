from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)


@dataclass(slots=True)
class FakeInfrastructureProvider:

    provider_name: str

    @property
    def name(self) -> str:
        return self.provider_name

    async def startup(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass


def test_registry_replaces_provider_with_same_name() -> None:
    registry = InfrastructureRegistry()

    first = FakeInfrastructureProvider(provider_name="cache")

    second = FakeInfrastructureProvider(provider_name="cache")

    registry.register(first)
    registry.register(second)

    provider = registry.get("cache")

    assert provider is second
