from __future__ import annotations

from template_app.runtime.container.models.scope import DependencyScope
from template_app.runtime.infrastructure.infra import CacheProvider


def test_provider_has_name() -> None:
    provider = CacheProvider(url="redis://localhost:6379")

    assert provider.name == "cache"


def test_provider_has_scope() -> None:
    provider = CacheProvider(url="redis://localhost:6379")

    assert provider.scope is DependencyScope.SINGLETON
