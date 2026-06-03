from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.dag import LifecycleDAGExecutor
from template_app.runtime.lifecycle.exceptions import LifecycleCycleError
from template_app.runtime.lifecycle.models import (
    LifecycleHook,
    RetryPolicy,
)


@pytest.mark.asyncio
async def test_executor_runs_hooks() -> None:
    events: list[str] = []

    async def first() -> None:
        events.append("first")

    async def second() -> None:
        events.append("second")

    hooks = (
        LifecycleHook(name="first", handler=first),
        LifecycleHook(name="second", handler=second),
    )

    executor = LifecycleDAGExecutor()
    await executor.execute(hooks)

    assert set(events) == {"first", "second"}


@pytest.mark.asyncio
async def test_executor_respects_dependencies() -> None:
    events: list[str] = []

    async def database() -> None:
        events.append("database")

    async def cache() -> None:
        events.append("cache")

    hooks = (
        LifecycleHook(name="database", handler=database),
        LifecycleHook(
            name="cache",
            handler=cache,
            dependencies=frozenset({"database"}),
        ),
    )

    executor = LifecycleDAGExecutor()
    await executor.execute(hooks)

    assert events == ["database", "cache"]


@pytest.mark.asyncio
async def test_executor_detects_cycle() -> None:
    async def noop() -> None:
        pass

    hooks = (
        LifecycleHook(
            name="a",
            handler=noop,
            dependencies=frozenset({"c"}),
        ),
        LifecycleHook(
            name="b",
            handler=noop,
            dependencies=frozenset({"a"}),
        ),
        LifecycleHook(
            name="c",
            handler=noop,
            dependencies=frozenset({"b"}),
        ),
    )

    executor = LifecycleDAGExecutor()

    with pytest.raises(LifecycleCycleError):
        await executor.execute(hooks)


@pytest.mark.asyncio
async def test_executor_retries_failed_hook() -> None:
    attempts = 0

    async def handler() -> None:
        nonlocal attempts
        attempts += 1

        if attempts < 2:
            raise RuntimeError("fail")

    hook = LifecycleHook(
        name="retry",
        handler=handler,
        retry_policy=RetryPolicy(
            retries=1,
            backoff_ms=0,
        ),
        critical=True,
    )

    executor = LifecycleDAGExecutor()
    await executor.execute((hook,))

    assert attempts == 2
