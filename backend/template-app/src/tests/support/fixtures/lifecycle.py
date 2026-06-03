from __future__ import annotations

import pytest

from template_app.runtime.lifecycle.registry import (
    LifecycleRegistry,
)


@pytest.fixture
def lifecycle_registry(runtime) -> LifecycleRegistry:
    """
    Return runtime lifecycle registry.
    """
    return runtime.lifecycle.registry


@pytest.fixture
async def running_kernel(kernel_harness):
    """
    Started runtime kernel.
    """
    await kernel_harness.startup()

    yield kernel_harness

    await kernel_harness.shutdown()
