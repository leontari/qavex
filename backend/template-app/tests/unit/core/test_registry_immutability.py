from __future__ import annotations

import pytest

from template_app.bootstrap.registry import ModuleRegistry


def test_registry_modules_are_immutable() -> None:
    registry = ModuleRegistry()

    modules = registry.modules

    with pytest.raises(AttributeError):
        modules.append(object())
