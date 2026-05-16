from __future__ import annotations

from template_app.bootstrap.runtime.registry import LifecycleRegistry


def test_registry_initial_state() -> None:
    registry = LifecycleRegistry()

    assert registry.startup_hooks == ()
    assert registry.shutdown_hooks == ()
