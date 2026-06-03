from __future__ import annotations

from template_app.runtime.lifecycle.models import LifecycleHook
from template_app.runtime.lifecycle.registry import LifecycleRegistry


def test_registry_registers_startup_hook() -> None:
    registry = LifecycleRegistry()

    async def startup() -> None:
        pass

    hook = LifecycleHook(
        name="startup",
        handler=startup,
    )

    registry.register_startup_hook(hook)

    assert hook in registry.startup_hooks


def test_registry_registers_shutdown_hook() -> None:
    registry = LifecycleRegistry()

    async def shutdown() -> None:
        pass

    hook = LifecycleHook(
        name="shutdown",
        handler=shutdown,
    )

    registry.register_shutdown_hook(hook)

    assert hook in registry.shutdown_hooks


def test_registry_registers_multiple_startup_hooks() -> None:
    registry = LifecycleRegistry()

    async def first() -> None:
        pass

    async def second() -> None:
        pass

    registry.register_startup_hooks(
        (
            LifecycleHook(name="first", handler=first),
            LifecycleHook(name="second", handler=second),
        )
    )

    assert len(registry.startup_hooks) == 2
