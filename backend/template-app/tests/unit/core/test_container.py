from __future__ import annotations

import pytest

from template_app.bootstrap.container import Container
from template_app.infrastructure.providers.cache import CacheProvider


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
