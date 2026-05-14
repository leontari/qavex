"""
Async background task management.

This module provides centralized management for long-running runtime tasks
such as:

- health schedulers
- metrics refreshers
- Kafka consumers
- distributed coordinators
- background synchronization loops

The task manager ensures:

- graceful shutdown
- cancellation safety
- runtime observability
"""

from __future__ import annotations

import asyncio
import logging


logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    """
    Runtime manager for async background tasks.
    """

    def __init__(self) -> None:
        """Initialize task manager."""
        self._tasks: set[asyncio.Task] = set()

    def create_task(
        self,
        coro: asyncio.coroutines,
        *,
        name: str,
    ) -> asyncio.Task:
        """
        Register and start a background task.

        Args:
            coro:
                Coroutine to execute.

            name:
                Human-readable task name.

        Returns:
            asyncio.Task:
                Registered async task.
        """
        task = asyncio.create_task(
            coro,
            name=name,
        )

        self._tasks.add(task)

        task.add_done_callback(self._tasks.discard)

        logger.info(
            "Background task started: %s",
            name,
        )

        return task

    async def shutdown(self) -> None:
        """Gracefully stop all background tasks."""
        if not self._tasks:
            return

        logger.info(
            "Stopping background tasks...",
        )

        for task in self._tasks:
            task.cancel()

        await asyncio.gather(
            *self._tasks,
            return_exceptions=True,
        )

        logger.info(
            "Background tasks stopped.",
        )
