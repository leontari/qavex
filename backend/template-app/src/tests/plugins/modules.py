from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.modules import ModuleRegistry
from template_app.runtime.modules.runtime import ModuleRuntime


@pytest.fixture
def module_runtime(kernel: RuntimeKernel) -> ModuleRuntime:
    """
    Module runtime domain.
    """
    return kernel.runtime.modules


@pytest.fixture
def module_registry(module_runtime: ModuleRuntime) -> ModuleRegistry:
    return module_runtime.registry
