from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class LifecycleManager:
    """Lifecycle orchestration manager."""

    registry: LifecycleRegistry

    async def startup(self) -> None:
        """Execute startup lifecycle hooks."""
        for hook in self.registry.startup_hooks:
            await hook.handler()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle hooks."""
        for hook in self.registry.shutdown_hooks:
            await hook.handler()
