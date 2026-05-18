from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from template_app.bootstrap.contracts.types import DependencyScope

if TYPE_CHECKING:
    from typing import Any


class DependencyProvider(Protocol):
    """Dependency provider contract."""

    @property
    def name(self) -> str:
        """Dependency name."""

    @property
    def scope(self) -> DependencyScope:
        """Dependency scope."""

    def provide(self) -> Any:
        """Build dependency instance."""
