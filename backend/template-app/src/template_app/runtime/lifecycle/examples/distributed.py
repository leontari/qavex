"""
Distributed lifecycle example.

Simulates multi-service / multi-runtime kernel orchestration.

Used for:
- microservices coordination
- multi-node startup simulation
- dependency-aware distributed systems
"""

from __future__ import annotations

from template_app.runtime.lifecycle.hooks import LifecycleHook


async def start_event_bus() -> None:  # noqa: RUF029, D103
    print("event bus started")  # noqa: T201


async def start_command_bus() -> None:  # noqa: RUF029, D103
    print("command bus started")  # noqa: T201


async def start_query_bus() -> None:  # noqa: RUF029, D103
    print("query bus started")  # noqa: T201


async def start_modules() -> None:  # noqa: RUF029, D103
    print("modules loaded")  # noqa: T201


def build_hooks() -> list[LifecycleHook]:
    """
    Build distributed runtime lifecycle graph.

    Returns:
        List of lifecycle hooks forming distributed DAG.

    """
    return [
        LifecycleHook(
            name="event-bus",
            handler=start_event_bus,
        ),
        LifecycleHook(
            name="command-bus",
            handler=start_command_bus,
            depends_on=frozenset({"event-bus"}),
        ),
        LifecycleHook(
            name="query-bus",
            handler=start_query_bus,
            depends_on=frozenset({"event-bus"}),
        ),
        LifecycleHook(
            name="modules",
            handler=start_modules,
            depends_on=frozenset({"command-bus", "query-bus"}),
        ),
    ]
