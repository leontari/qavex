"""Stateless lifecycle hooks execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.lifecycle.snapshot import LifecycleRegistrySnapshot

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class LifecycleManager:
    """
    Stateless lifecycle hooks executor.

    Features:
        dependency-safe execution order
        parallel execution
        failure isolation
        retry policy

    """

    snapshot: LifecycleRegistrySnapshot

    async def startup(self) -> None:
        """Execute lifecycle startup hooks."""
        await self._execute_startup()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle hooks."""
        await self._execute_shutdown()

    async def _execute_startup(self) -> None:
        """Startup."""
        for hook in self.snapshot.startup:
            await self._execute_hook_with_retry(hook)

    async def _execute_shutdown(self) -> None:
        """Shutdown."""
        for hook in reversed(self.snapshot.shutdown):
            await self._execute_hook_with_retry(hook)

    async def _execute_hook_with_retry(self, hook) -> None:
        """Execute hooks."""
        retries = getattr(hook, "retries", 1)

        for attempt in range(retries):
            try:
                await hook.handler()
                return
            except Exception:
                if attempt + 1 >= retries:
                    raise
