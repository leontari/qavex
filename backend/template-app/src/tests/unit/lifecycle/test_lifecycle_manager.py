from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.hooks import LifecycleHook
from template_app.runtime.lifecycle.manager import LifecycleManager
from template_app.runtime.lifecycle.registry import LifecycleRegistry


@pytest.mark.asyncio
async def test_manager_executes_startup_hooks() -> None:
    registry = LifecycleRegistry()

    state = {"started": False}

    async def startup() -> None:
        state["started"] = True

    registry.register_startup(
        LifecycleHook(
            name="startup",
            handler=startup,
        ),
    )

    manager = LifecycleManager(registry=registry)

    await manager.startup()

    assert state["started"] is True


@pytest.mark.asyncio
async def test_manager_executes_shutdown_hooks() -> None:
    registry = LifecycleRegistry()

    state = {"shutdown": False}

    async def shutdown() -> None:
        state["shutdown"] = True

    registry.register_shutdown(
        LifecycleHook(
            name="shutdown",
            handler=shutdown,
        ),
    )

    manager = LifecycleManager(registry=registry)

    await manager.shutdown()

    assert state["shutdown"] is True


async def test_lifecycle_manager_executes_hooks() -> None:
    registry = LifecycleRegistry()

    state: dict[str, bool] = {
        "started": False,
        "stopped": False,
    }

    async def startup() -> None:
        state["started"] = True

    async def shutdown() -> None:
        state["stopped"] = True

    registry.register_startup(
        LifecycleHook(
            name="startup",
            handler=startup,
        ),
    )

    registry.register_shutdown(
        LifecycleHook(
            name="shutdown",
            handler=shutdown,
        ),
    )

    manager = LifecycleManager(registry)

    await manager.startup()
    await manager.shutdown()

    assert state["started"] is True
    assert state["stopped"] is True
