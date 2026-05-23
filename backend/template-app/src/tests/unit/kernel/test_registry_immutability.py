from __future__ import annotations

import pytest

from template_app.runtime.module import ModuleRegistry
from template_app.runtime.lifecycle import LifecycleRegistry


def test_registry_lists_are_immutable() -> None:
    registry = LifecycleRegistry()

    assert isinstance(registry.startup_hooks, tuple)
    assert isinstance(registry.shutdown_hooks, tuple)


def test_registry_modules_are_immutable() -> None:
    registry = ModuleRegistry()

    modules = registry.modules

    with pytest.raises(AttributeError):
        modules.append(object())
