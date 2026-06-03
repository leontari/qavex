"""Provider Example."""

from __future__ import annotations

from dataclasses import dataclass, field

from template_app.runtime.infrastructure.infra.cache.client import CacheClient
from template_app.runtime.container.types import DependencyScope


@dataclass(slots=True)
class CacheProvider:
    """Cache infrastructure provider."""

    url: str

    client: CacheClient | None = field(
        default=None,
        init=False,
    )

    started: bool = field(
        default=False,
        init=False,
    )

    @property
    def name(self) -> str:
        return "cache"

    @property
    def scope(self) -> DependencyScope:
        return DependencyScope.SINGLETON

    async def startup(self) -> None:
        self.client = CacheClient(url=self.url)
        self.started = True

    async def shutdown(self) -> None:
        self.started = False
