from __future__ import annotations

import pytest

from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.mark.asyncio
async def test_kernel_starts_installed_transport(
    kernel_harness: KernelTestHarness,
    transport,
) -> None:
    """
    Runtime kernel should start up transports.
    """
    await kernel_harness.startup()


@pytest.mark.asyncio
async def test_kernel_shutdowns_installed_transport(
    kernel_harness: KernelTestHarness,
    transport,
) -> None:
    """
    Runtime kernel should shut down transports.
    """
    await kernel_harness.shutdown()
