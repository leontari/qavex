"""Provider Registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.contracts import InfrastructureProvider


@dataclass(slots=True)
class InfrastructureRegistry:
    """Infrastructure provider registry."""

    _providers: dict[str, InfrastructureProvider] = field(
        default_factory=dict,
    )

    def register(self, provider: InfrastructureProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> InfrastructureProvider:
        return self._providers[name]

    # TODO: check typing - looks OK
    @property
    def providers(self) -> tuple[InfrastructureProvider, ...]:
        return tuple(self._providers.values())
