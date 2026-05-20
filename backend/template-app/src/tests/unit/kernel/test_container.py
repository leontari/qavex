from __future__ import annotations

from dataclasses import dataclass

import pytest

from template_app.bootstrap.contracts import DependencyScope
from template_app.bootstrap.contracts.dependencies import DependencyProvider
from template_app.bootstrap.kernel.container import Container
from template_app.infrastructure.cache import CacheProvider


@dataclass(slots=True)
class FakeProvider:
    value: str

    @property
    def name(self) -> str:
        return "fake"

    @property
    def scope(self) -> DependencyScope:
        return DependencyScope.SINGLETON

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


def test_container_registers_dependency() -> None:
    container = Container()

    provider = CacheProvider(url="redis://localhost")

    container.register(provider)

    resolved = container.resolve("cache")

    assert resolved is provider


def test_container_raises_for_missing_dependency() -> None:
    container = Container()

    with pytest.raises(LookupError):
        container.resolve("missing")



def test_container_returns_readonly_mapping() -> None:
    container = Container()

    provider = CacheProvider(
        url="redis://localhost",
    )

    container.register(provider)

    dependencies = container.dependencies

    assert "cache" in dependencies
