from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.fakes.transports import FakeTransport


def test_kernel_installs_transport(kernel: RuntimeKernel) -> None:
    """
    Kernel should own transport installation.
    """
    transport = FakeTransport(name="fake")
    kernel.install_transport(transport)

    assert transport in kernel.transports


@pytest.mark.asyncio
async def test_kernel_starts_transports(kernel: RuntimeKernel) -> None:
    """
    Kernel startup should startup transports.
    """
    transport = FakeTransport(name="fake")
    kernel.install_transport(transport)

    await kernel.startup()

    assert transport.started is True


@pytest.mark.asyncio
async def test_kernel_shutdowns_transports(kernel: RuntimeKernel) -> None:
    """
    Kernel shutdown should shut down transports.
    """
    transport = FakeTransport(name="fake")
    kernel.install_transport(transport)

    await kernel.shutdown()

    assert transport.stopped is True
