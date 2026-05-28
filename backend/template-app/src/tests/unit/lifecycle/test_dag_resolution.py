from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.dag import (
    LifecycleDAGExecutor,
)
from template_app.runtime.lifecycle.exceptions import (
    LifecycleCycleError,
)
from template_app.runtime.lifecycle.hooks import (
    LifecycleHook,
)


async def _noop() -> None:
    """No-op async hook."""


def build_hook(
    name: str,
    *,
    after: tuple[str, ...] = (),
) -> LifecycleHook:
    """Build lifecycle hook."""

    return LifecycleHook(
        name=name,
        handler=_noop,
        after=after,
    )


def test_dag_resolves_linear_dependencies() -> None:
    """
    DAG should resolve linear dependency chain.

    Expected:
        database -> cache -> api
    """

    dag = LifecycleDAGExecutor()

    database = build_hook("database")

    cache = build_hook(
        "cache",
        after=("database",),
    )

    api = build_hook(
        "api",
        after=("cache",),
    )

    resolved = dag.resolve(
        (
            api,
            cache,
            database,
        ),
    )

    assert [hook.name for hook in resolved] == [
        "database",
        "cache",
        "api",
    ]


def test_dag_resolves_parallel_dependencies() -> None:
    """
    DAG should resolve parallel branches.
    """

    dag = LifecycleDAG()

    database = build_hook("database")

    cache = build_hook(
        "cache",
        after=("database",),
    )

    queue = build_hook(
        "queue",
        after=("database",),
    )

    resolved = dag.resolve(
        (
            cache,
            queue,
            database,
        ),
    )

    names = [hook.name for hook in resolved]

    assert names[0] == "database"

    assert set(names[1:]) == {
        "cache",
        "queue",
    }


def test_dag_detects_cycle() -> None:
    """
    DAG should detect dependency cycle.
    """

    dag = LifecycleDAG()

    a = build_hook(
        "a",
        after=("c",),
    )

    b = build_hook(
        "b",
        after=("a",),
    )

    c = build_hook(
        "c",
        after=("b",),
    )

    with pytest.raises(
        LifecycleCycleError,
    ):
        dag.resolve(
            (
                a,
                b,
                c,
            ),
        )


def test_dag_allows_independent_hooks() -> None:
    """
    DAG should allow hooks without dependencies.
    """

    dag = LifecycleDAGExecutor()

    a = build_hook("a")
    b = build_hook("b")
    c = build_hook("c")

    resolved = dag.resolve(
        (
            a,
            b,
            c,
        ),
    )

    assert len(resolved) == 3

    assert {
        hook.name
        for hook in resolved
    } == {
        "a",
        "b",
        "c",
    }


def test_dag_preserves_dependency_order() -> None:
    """
    DAG should preserve dependency ordering guarantees.
    """

    dag = LifecycleDAG()

    core = build_hook("core")

    transport = build_hook(
        "transport",
        after=("core",),
    )

    observability = build_hook(
        "observability",
        after=("core",),
    )

    api = build_hook(
        "api",
        after=(
            "transport",
            "observability",
        ),
    )

    resolved = dag.resolve(
        (
            api,
            observability,
            transport,
            core,
        ),
    )

    names = [
        hook.name
        for hook in resolved
    ]

    assert names.index("core") < names.index("transport")

    assert names.index("core") < names.index(
        "observability",
    )

    assert names.index("transport") < names.index(
        "api",
    )

    assert names.index("observability") < names.index(
        "api",
    )
