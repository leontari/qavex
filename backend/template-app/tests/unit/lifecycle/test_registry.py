from __future__ import annotations

from template_app.bootstrap.lifecycle.hooks import LifecycleHook
from template_app.bootstrap.lifecycle.registry import LifecycleRegistry


async def startup_handler() -> None:
    return None


async def shutdown_handler() -> None:
    return None


def test_registry_initial_state() -> None:
    registry = LifecycleRegistry()

    assert registry.startup_hooks == ()
    assert registry.shutdown_hooks == ()


def test_registry_registers_startup_hook() -> None:
    registry = LifecycleRegistry()

    hook = LifecycleHook(name="startup", handler=startup_handler)

    registry.register_startup(hook)

    assert len(registry.startup_hooks) == 1
    assert registry.startup_hooks[0] is hook


def test_registry_registers_shutdown_hook() -> None:
    registry = LifecycleRegistry()

    hook = LifecycleHook(name="shutdown", handler=shutdown_handler)

    registry.register_shutdown(hook)

    assert len(registry.shutdown_hooks) == 1
    assert registry.shutdown_hooks[0] is hook


def test_registry_returns_immutable_snapshots() -> None:
    registry = LifecycleRegistry()

    snapshot = registry.startup_hooks

    assert isinstance(snapshot, tuple)
