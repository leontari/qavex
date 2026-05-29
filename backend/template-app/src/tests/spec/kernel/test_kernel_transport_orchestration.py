from __future__ import annotations

import pytest

from tests.support.fakes.transports import FakeTransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_kernel_installs_transport(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should own transport installation.
    """
    transport = FakeTransport(name="fake")

    kernel_harness.install_transport(transport)

    assert transport in kernel_harness.kernel.transports


@pytest.mark.asyncio
async def test_kernel_starts_transports(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel startup should startup transports.
    """
    transport = FakeTransport(name="fake")

    kernel_harness.install_transport(transport)

    await kernel_harness.startup()

    assert transport.started is True


@pytest.mark.asyncio
async def test_kernel_shutdowns_transports(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel shutdown should shut down transports.
    """
    transport = FakeTransport(name="fake")

    kernel_harness.install_transport(transport)

    await kernel_harness.shutdown()

    assert transport.stopped is True
