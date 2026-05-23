"""Provider Registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .contracts import InfrastructureProvider


@dataclass(slots=True)
class InfrastructureRegistry:
    """Infrastructure provider registry."""

    _providers: dict[str, InfrastructureProvider] = field(
        default_factory=dict,
    )

    def register(self, provider: InfrastructureProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> InfrastructureProvider:
        try:
            return self._providers[name]
        except KeyError as e:
            msg = f"Infrastructure provider not found: {name}"
            raise LookupError(msg) from e

    # TODO: check typing - looks OK
    @property
    def providers(self) -> tuple[InfrastructureProvider, ...]:
        return tuple(self._providers.values())
