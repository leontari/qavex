from __future__ import annotations

from template_app.bootstrap.runtime.hooks import LifecycleHook
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry

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
