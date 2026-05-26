"""Lifecycle DAG execution."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING

from template_app.runtime.lifecycle.exceptions import (
    LifecycleCycleError,
    LifecycleHookExecutionError,
)

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.models import LifecycleHook


class LifecycleDAGExecutor:
    """
    Lifecycle DAG executor.

    Responsibilities:
        - dependency graph execution
        - parallel stage execution
        - cycle detection
        - retry-aware execution
    """

    async def _execute_hook(self, hook: LifecycleHook) -> None:  # noqa: PLR6301
        """
        Execute lifecycle hook with retry policy.

        Raises:
            LifecycleHookExecutionError:
                If hook is critical and all retries failed.

        """
        retries = hook.retry_policy.retries + 1
        last_error: Exception | None = None

        for attempt in range(retries):
            try:
                await hook.handler()
            except (RuntimeError, TimeoutError) as exc:
                # retryable errors ONLY (safe category)
                last_error = exc

                if attempt == retries - 1:
                    break

                await asyncio.sleep(hook.retry_policy.backoff_ms / 1000)
            else:
                return

        if hook.critical and last_error:
            msg = (
                f"Hook '{hook.name}' failed after {retries} attempts "
                f"(critical={hook.critical})"
            )
            raise LifecycleHookExecutionError(msg) from last_error

    async def execute(self, hooks: tuple[LifecycleHook, ...]) -> None:
        """Execute hooks."""
        graph: dict[str, set[str]] = defaultdict(set)
        indegree: dict[str, int] = {hook.name: 0 for hook in hooks}
        hook_map = {hook.name: hook for hook in hooks}

        # build graph
        for hook in hooks:
            for dependency in hook.dependencies:
                graph[dependency].add(hook.name)
                indegree[hook.name] += 1

        queue = [name for name, degree in indegree.items() if degree == 0]
        executed = 0

        while queue:
            current_stage = queue.copy()
            queue.clear()

            await asyncio.gather(*[
                self._execute_hook(hook_map[name]) for name in current_stage
            ])

            executed += len(current_stage)

            for node in current_stage:
                for dependent in graph[node]:
                    indegree[dependent] -= 1
                    if indegree[dependent] == 0:
                        queue.append(dependent)

        if executed != len(hooks):
            msg = "Lifecycle DAG contains cycle."
            raise LifecycleCycleError(msg)
