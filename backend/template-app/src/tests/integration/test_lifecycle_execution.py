from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.hooks import LifecycleHook
from template_app.runtime.lifecycle.manager import LifecycleManager
from template_app.runtime.lifecycle.registry import LifecycleRegistry


@pytest.mark.asyncio
async def test_startup_hooks_execute_in_order() -> None:
    registry = LifecycleRegistry()

    events: list[str] = []

    async def first() -> None:
        events.append("first")

    async def second() -> None:
        events.append("second")

    registry.register_startup(
        LifecycleHook(
            name="first",
            handler=first,
        ),
    )

    registry.register_startup(
        LifecycleHook(
            name="second",
            handler=second,
        ),
    )

    manager = LifecycleManager(registry=registry)

    await manager.startup()

    assert events == ["first", "second"]


@pytest.mark.asyncio
async def test_shutdown_hooks_execute_in_order() -> None:
    registry = LifecycleRegistry()

    events: list[str] = []

    async def first() -> None:
        events.append("first")

    async def second() -> None:
        events.append("second")

    registry.register_shutdown(
        LifecycleHook(
            name="first",
            handler=first,
        ),
    )

    registry.register_shutdown(
        LifecycleHook(
            name="second",
            handler=second,
        ),
    )

    manager = LifecycleManager(registry=registry)

    await manager.shutdown()

    assert events == ["first", "second"]
