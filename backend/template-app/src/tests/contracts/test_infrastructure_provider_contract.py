from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.contracts import InfrastructureProvider


@dataclass(slots=True)
class FakeInfrastructureProvider:

    @property
    def name(self) -> str:
        return "fake"

    async def startup(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass


def test_infrastructure_provider_contract() -> None:
    provider: InfrastructureProvider = FakeInfrastructureProvider()

    assert provider.name == "fake"
