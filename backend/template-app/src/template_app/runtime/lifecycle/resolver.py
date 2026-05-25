from __future__ import annotations

from collections import defaultdict, deque
from typing import TYPE_CHECKING

from template_app.runtime.lifecycle.graph import LifecycleGraph
from template_app.runtime.lifecycle.hooks import LifecycleHook

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.hooks import LifecycleHook


class LifecycleResolutionError(RuntimeError):
    pass


def resolve_execution_order(
    graph: LifecycleGraph,
) -> tuple[LifecycleHook, ...]:
    """Resolve DAG execution order using topological sort."""
    hooks = {hook.name: hook for hook in graph.hooks}

    indegree: dict[str, int] = defaultdict(int)

    adjacency: dict[str, set[str]] = defaultdict(set)

    for hook in graph.hooks:
        for dependency in hook.depends_on:
            if dependency not in hooks:
                msg = f"Unknown dependency: {dependency}"
                raise LifecycleResolutionError(msg)

            adjacency[dependency].add(hook.name)

            indegree[hook.name] += 1

    queue = deque([
        hook.name for hook in graph.hooks if indegree[hook.name] == 0
    ])

    resolved: list[LifecycleHook] = []

    while queue:
        current = queue.popleft()

        resolved.append(hooks[current])

        for neighbor in adjacency[current]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(resolved) != len(graph.hooks):
        msg_0 = "Lifecycle graph contains cycle."
        raise LifecycleResolutionError(msg_0)

    return tuple(resolved)
