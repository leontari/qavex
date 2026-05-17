"""Provider Example."""

from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.contracts.types import DependencyScope


@dataclass(slots=True)
class CacheClient:
    url: str


@dataclass(slots=True)
class CacheProvider:
    """Cache provider."""

    url: str

    @property
    def name(self) -> str:
        return "cache"

    @property
    def scope(self) -> DependencyScope:
        return DependencyScope.SINGLETON

    def provide(self) -> CacheClient:
        return CacheClient(url=self.url)
