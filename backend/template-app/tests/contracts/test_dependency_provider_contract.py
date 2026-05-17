from __future__ import annotations

from template_app.core.types import DependencyScope
from template_app.infrastructure.providers.cache import CacheProvider


def test_provider_has_name() -> None:
    provider = CacheProvider(url="redis://localhost")

    assert provider.name == "cache"


def test_provider_has_scope() -> None:
    provider = CacheProvider(url="redis://localhost")

    assert provider.scope is DependencyScope.SINGLETON
