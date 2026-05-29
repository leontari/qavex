from __future__ import annotations

import pytest

from template_app.runtime.modules import ModuleRegistry
from template_app.runtime.modules.runtime import ModuleRuntime
from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.fixture
def module_runtime(kernel_harness: KernelTestHarness) -> ModuleRuntime:
    """
    Module runtime domain.
    """
    return kernel_harness.modules


@pytest.fixture
def module_registry(module_runtime: ModuleRuntime) -> ModuleRegistry:
    return module_runtime.registry
