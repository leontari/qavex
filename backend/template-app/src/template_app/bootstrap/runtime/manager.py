from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.runtime.registry import LifecycleRegistry


class LifecycleManager:
    """Executes runtime lifecycle hooks."""

    def __init__(self, registry: LifecycleRegistry) -> None:
        self.registry = registry

    async def startup(self) -> None:
        """Execute startup lifecycle hooks."""
        for hook in self.registry.startup_hooks:
            await hook.handler()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle hooks."""
        for hook in self.registry.shutdown_hooks:
            await hook.handler()
