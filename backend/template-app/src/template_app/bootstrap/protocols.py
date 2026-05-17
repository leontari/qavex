from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any

    from template_app.bootstrap.module_context import ModuleSetupContext
    from template_app.core.types import DependencyScope


class ModuleProtocol(Protocol):
    """
    Contract for application modules.

    Every module is responsible for registering its own:

    - routes
    - dependencies
    - event handlers
    - runtime hooks
    - background tasks

    Modules must NOT create infrastructure resources directly.
    They receive them through the application context container.
    """

    def setup(self, context: ModuleSetupContext) -> None:
        """Configure module."""


class DependencyProvider(Protocol):
    """Dependency provider contract."""

    @property
    def name(self) -> str:
        """Provider name."""

    @property
    def scope(self) -> DependencyScope:
        """Dependency lifecycle scope."""

    # TODO: check any typing
    def provide(self) -> Any:
        """Build dependency."""
