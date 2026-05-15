from __future__ import annotations

from template_app.bootstrap.runtime.hooks import (
    LifecycleHook,
)
from template_app.bootstrap.runtime.registry import (
    LifecycleRegistry,
)


async def fake_hook() -> None:
    return None


def test_register_startup_hook() -> None:
    registry = LifecycleRegistry()

    hook = LifecycleHook(
        name="startup",
        handler=fake_hook,
    )

    registry.register_startup(hook)

    assert registry.startup_hooks == (hook,)



def test_register_shutdown_hook() -> None:
    registry = LifecycleRegistry()

    hook = LifecycleHook(
        name="shutdown",
        handler=fake_hook,
    )

    registry.register_shutdown(hook)

    assert registry.shutdown_hooks == (hook,)
