from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.contracts import DependencyProvider


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
        """Register provider."""
        self._providers[provider.name] = provider

    def resolve(self, key: str) -> DependencyProvider:
        """Resolve provider."""
        try:
            return self._providers[key]

        except KeyError as error:
            msg = f"Dependency '{key}' not found."
            raise LookupError(msg) from error

    def contains(self, key: str) -> bool:
        """Check provider existence."""
        return key in self._providers

    @property
    def providers(self) -> tuple[DependencyProvider, ...]:
        """Immutable providers snapshot."""
        return tuple(self._providers.values())
