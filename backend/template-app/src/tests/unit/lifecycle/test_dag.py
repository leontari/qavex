from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.dag import (
    LifecycleDAGExecutor,
)
from template_app.runtime.lifecycle.models import (
    LifecycleHook,
)


@pytest.mark.asyncio
async def test_dag_executes_dependencies() -> None:

    execution: list[str] = []

    async def database() -> None:
        execution.append("database")

    async def cache() -> None:
        execution.append("cache")

    async def api() -> None:
        execution.append("api")

    hooks = (
        LifecycleHook(
            name="database",
            handler=database,
        ),
        LifecycleHook(
            name="cache",
            handler=cache,
        ),
        LifecycleHook(
            name="api",
            handler=api,
            dependencies=frozenset({
                "database",
                "cache",
            }),
        ),
    )

    executor = LifecycleDAGExecutor()

    await executor.execute(hooks)

    assert execution.index("database") < execution.index("api")
    assert execution.index("cache") < execution.index("api")
