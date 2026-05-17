from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.protocols import DependencyProvider


@dataclass(slots=True)
class Container:
    """
    Runtime dependency container.

    Container is used for:
    - runtime service registry;
    - application runtime dependency graph.

    Stores runtime services and infrastructure adapters.

    FastAPI DI and Runtime DI are separated from each other.
    FastAPI DI is used only as transport-layer dependency injection.
    """

    _providers: dict[str, DependencyProvider] = field(default_factory=dict)

    def register(self, provider: DependencyProvider) -> None:
        """Register dependency provider."""
        self._providers[provider.name] = provider

    def resolve(self, key: str) -> DependencyProvider:
        """Resolve dependency."""
        try:
            return self._providers[key]

        except KeyError as error:
            msg = f"Dependency '{key}' not found."
            raise LookupError(msg) from error

    def contains(self, key: str) -> bool:
        """Check dependency existence."""
        return key in self._providers

    @property
    def dependencies(self) -> dict[str, DependencyProvider]:
        """Readonly dependency mapping."""
        return dict(self._providers)
