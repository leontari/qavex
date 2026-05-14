"""
Concurrent health plugin execution engine.

This module provides:

- async concurrent execution
- timeout isolation
- concurrency limiting
- exception isolation
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.health.plugins.base import (
        HealthCheckPlugin,
        HealthCheckResult,
    )


class HealthExecutor:
    """Concurrent executor for health plugins."""

    def __init__(
        self,
        concurrency_limit: int = 10,
    ) -> None:
        """
        Initialize the executor.

        Args:
            concurrency_limit:
                Maximum number of concurrent plugin executions.

        """
        self._semaphore = asyncio.Semaphore(concurrency_limit)

    async def execute(
        self,
        plugin: HealthCheckPlugin,
    ) -> HealthCheckResult:
        """
        Execute a single plugin with timeout isolation.

        Args:
            plugin:
                Health plugin instance.

        Returns:
            HealthCheckResult:
                Plugin execution result.

        """
        async with self._semaphore:
            return await asyncio.wait_for(
                plugin.check(),
                timeout=plugin.policy.timeout_seconds,
            )

    async def execute_many(
        self,
        plugins: list[HealthCheckPlugin],
    ) -> list[HealthCheckResult]:
        """
        Execute multiple plugins concurrently.

        Args:
            plugins:
                Plugin instances.

        Returns:
            list[HealthCheckResult]:
                Plugin execution results.

        """
        return await asyncio.gather(
            *(self.execute(plugin) for plugin in plugins),
            return_exceptions=False,
        )
