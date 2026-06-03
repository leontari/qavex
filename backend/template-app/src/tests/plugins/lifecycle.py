from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.fakes.lifecycle import FakeLifecycleHook


@pytest.fixture
def startup_hook() -> FakeLifecycleHook:
    """
    Return fake startup hook.
    """
    return FakeLifecycleHook()


@pytest.fixture
def shutdown_hook() -> FakeLifecycleHook:
    """
    Return fake shutdown hook.
    """
    return FakeLifecycleHook()


@pytest.fixture
async def started_kernel(kernel: RuntimeKernel) -> AsyncIterator:
    """
    Started runtime harness.
    """
    await kernel.startup()

    yield kernel

    await kernel.shutdown()
