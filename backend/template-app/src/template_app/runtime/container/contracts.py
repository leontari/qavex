"""DI contracts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any

    from .manager import DependencyManager
    from .types import DependencyScope


class DependencyProvider(Protocol):
    """Dependency provider contract."""

    scope: DependencyScope

    @property
    def scope(self) -> DependencyScope:
        """Dependency scope."""

    def provide(self, manager: DependencyManager) -> Any:
        """
        Build dependency instance.

        Returns:
            Dependency instance.

        """
