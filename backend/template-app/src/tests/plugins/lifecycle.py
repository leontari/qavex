from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from tests.support.fakes.lifecycle import FakeLifecycleHook
from tests.support.harness.kernel_test_harness import KernelTestHarness


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
async def started_kernel(kernel_harness: KernelTestHarness) -> AsyncIterator:
    """
    Started runtime harness.
    """
    await kernel_harness.startup()

    yield kernel_harness

    await kernel_harness.shutdown()
