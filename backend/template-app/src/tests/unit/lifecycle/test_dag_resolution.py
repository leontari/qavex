from template_app.runtime.lifecycle import LifecycleHook
from template_app.runtime.lifecycle.executor import LifecycleExecutor
from template_app.runtime.lifecycle.graph import LifecycleGraph
from template_app.runtime.lifecycle.resolver import resolve_execution_order, \
    LifecycleResolutionError


def test_resolver_orders_dependencies():

    db = LifecycleHook(
        name="db",
        handler=lambda: None,
    )

    cache = LifecycleHook(
        name="cache",
        handler=lambda: None,
        depends_on=frozenset({"db"}),
    )

    graph = LifecycleGraph(
        hooks=(cache, db),
    )

    ordered = resolve_execution_order(graph)

    assert ordered[0].name == "db"
    assert ordered[1].name == "cache"


import pytest


def test_cycle_detection():

    a = LifecycleHook(
        name="a",
        handler=lambda: None,
        depends_on=frozenset({"b"}),
    )

    b = LifecycleHook(
        name="b",
        handler=lambda: None,
        depends_on=frozenset({"a"}),
    )

    graph = LifecycleGraph(
        hooks=(a, b),
    )

    with pytest.raises(LifecycleResolutionError):
        resolve_execution_order(graph)


import pytest


@pytest.mark.asyncio
async def test_retry_policy():

    attempts = 0

    async def flaky():
        nonlocal attempts

        attempts += 1

        if attempts < 2:
            raise RuntimeError

    hook = LifecycleHook(
        name="flaky",
        handler=flaky,
        retries=2,
    )

    executor = LifecycleExecutor(
        graph=LifecycleGraph(hooks=(hook,)),
    )

    await executor.startup()

    assert attempts == 2
