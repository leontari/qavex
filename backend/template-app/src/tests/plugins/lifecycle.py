from __future__ import annotations

from typing import Any, AsyncGenerator

import pytest

from template_app.runtime.lifecycle.runtime import LifecycleRuntime
from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.fixture
def lifecycle(kernel_harness: KernelTestHarness) -> LifecycleRuntime:
    """
    Lifecycle runtime domain.
    """
    return kernel_harness.lifecycle


@pytest.fixture
async def started_kernel(
    kernel_harness: KernelTestHarness
) -> AsyncGenerator[KernelTestHarness, Any]:
    """
    Started runtime harness.
    """
    await kernel_harness.startup()

    yield kernel_harness

    await kernel_harness.shutdown()
