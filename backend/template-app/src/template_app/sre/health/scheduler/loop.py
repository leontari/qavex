"""
Background health scheduler loop.

This module implements the runtime scheduler responsible for:

- periodic health refresh
- background concurrent execution
- cached probe updates
- graceful shutdown
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.scheduler.executor import HealthExecutor
    from template_app.health.plugins.registry import HealthPluginRegistry


class HealthScheduler:
    """Background scheduler for health plugins."""

    def __init__(
        self,
        registry: HealthPluginRegistry,
        executor: HealthExecutor,
        interval_seconds: int = 10,
    ) -> None:
        """
        Initialize the scheduler.

        Args:
            registry:
                Plugin registry.

            executor:
                Plugin execution engine.

            interval_seconds:
                Scheduler refresh interval.

        """
        self.registry = registry
        self.executor = executor

        self.interval_seconds = interval_seconds

        self._task: asyncio.Task[None] | None = None
        self._running = False

    async def start(self) -> None:
        """Start the background scheduler loop."""
        if self._running:
            return

        self._running = True

        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        """Stop the background scheduler loop gracefully."""
        self._running = False

        if self._task is None:
            return

        self._task.cancel()

        try:
            await self._task
        except asyncio.CancelledError:
            pass

    async def refresh(self) -> None:
        """Execute a single scheduler refresh cycle."""
        plugins = self.registry.get_all()

        await self.executor.execute_many(plugins)

    async def _run(self) -> None:
        """Execute the scheduler loop continuously."""
        while self._running:
            await self.refresh()

            try:
                await asyncio.sleep(self.interval_seconds)

            except asyncio.CancelledError:
                break
