"""
Basic lifecycle DAG example.

Demonstrates simple dependency-based startup ordering
without transports or distributed runtime.
"""

from __future__ import annotations

from template_app.runtime.lifecycle.hooks import LifecycleHook


async def start_database() -> None:
    print("database started")  # noqa: T201


async def start_cache() -> None:
    print("cache started")  # noqa: T201


async def start_http() -> None:
    print("http started")  # noqa: T201


def build_hooks() -> list[LifecycleHook]:
    """
    Build basic lifecycle graph.

    Returns:
        List of lifecycle hooks forming a DAG.

    """
    return [
        LifecycleHook(
            name="database",
            handler=start_database,
        ),
        LifecycleHook(
            name="cache",
            handler=start_cache,
            depends_on=frozenset({"database"}),
        ),
        LifecycleHook(
            name="http",
            handler=start_http,
            depends_on=frozenset({"database", "cache"}),
        ),
    ]
