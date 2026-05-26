"""
Transport lifecycle example.

Demonstrates how HTTP, Kafka, CLI, gRPC
are coordinated via lifecycle DAG.

This is Kubernetes-grade boot orchestration model.
"""

from __future__ import annotations

from template_app.runtime.lifecycle.hooks import LifecycleHook


async def start_database() -> None:  # noqa: D103, RUF029
    print("database ready")  # noqa: T201


async def start_cache() -> None:  # noqa: D103, RUF029
    print("cache ready")  # noqa: T201


async def start_kafka() -> None:  # noqa: D103, RUF029
    print("kafka consumer started")  # noqa: T201


async def start_grpc() -> None:  # noqa: D103, RUF029
    print("gRPC server started")  # noqa: T201


async def start_http() -> None:  # noqa: D103, RUF029
    print("HTTP server started")  # noqa: T201


async def start_cli() -> None:  # noqa: D103, RUF029
    print("CLI runtime ready")  # noqa: T201


def build_hooks() -> list[LifecycleHook]:
    """
    Build transport-aware lifecycle DAG.

    This simulates production multi-runtime kernel:

    - HTTP API server
    - Kafka consumer worker
    - gRPC server
    - CLI mode runtime

    Returns:
        List of lifecycle hooks forming transport DAG.

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
            name="kafka",
            handler=start_kafka,
            depends_on=frozenset({"database"}),
        ),
        LifecycleHook(
            name="grpc",
            handler=start_grpc,
            depends_on=frozenset({"database", "cache"}),
        ),
        LifecycleHook(
            name="http",
            handler=start_http,
            depends_on=frozenset({"database", "cache"}),
        ),
        LifecycleHook(
            name="cli",
            handler=start_cli,
            depends_on=frozenset({"database"}),
        ),
    ]
