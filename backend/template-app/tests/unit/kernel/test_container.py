from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.contracts.dependencies import (
    DependencyProvider,
)
from template_app.bootstrap.kernel.container import Container


@dataclass(slots=True)
class FakeProvider:
    value: str

    @property
    def name(self) -> str:
        return "fake"

    def provide(self) -> str:
        return self.value



def test_container_registers_provider() -> None:
    container = Container()

    provider: DependencyProvider = FakeProvider("hello")

    container.register(provider)

    resolved = container.resolve("fake")

    assert resolved is provider



def test_container_contains_provider() -> None:
    container = Container()

    provider: DependencyProvider = FakeProvider("hello")

    container.register(provider)

    assert container.contains("fake") is True



def test_container_returns_immutable_snapshot() -> None:
    container = Container()

    provider: DependencyProvider = FakeProvider("hello")

    container.register(provider)

    snapshot = container.providers

    assert isinstance(snapshot, tuple)
    assert len(snapshot) == 1
