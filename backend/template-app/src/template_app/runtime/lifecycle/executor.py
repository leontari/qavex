from __future__ import annotations

import asyncio
from dataclasses import dataclass

from template_app.runtime.lifecycle.graph import LifecycleGraph
from template_app.runtime.lifecycle.resolver import resolve_execution_order


@dataclass(slots=True)
class LifecycleExecutor:
    """DAG lifecycle executor."""

    graph: LifecycleGraph

    async def startup(self) -> None:

        ordered = resolve_execution_order(
            self.graph,
        )

        for hook in ordered:
            await self._execute_hook(hook)

    async def shutdown(self) -> None:

        ordered = reversed(
            resolve_execution_order(
                self.graph,
            )
        )

        for hook in ordered:
            await self._execute_hook(hook)

    async def _execute_hook(self, hook) -> None:

        for attempt in range(hook.retries):
            try:
                await hook.handler()
                return

            except Exception:
                if attempt + 1 >= hook.retries:
                    if hook.critical:
                        raise
