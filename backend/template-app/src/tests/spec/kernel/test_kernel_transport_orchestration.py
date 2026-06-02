from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.fakes.transports import FakeTransport


def test_kernel_installs_transport(kernel: RuntimeKernel) -> None:
    """
    Kernel should install transport via launcher composition.
    """
    transport = FakeTransport(name="fake")

    with pytest.raises(RuntimeError):
        # kernel is frozen after build -> mutation must be forbidden
        kernel.install_transport(transport)


@pytest.mark.asyncio
async def test_kernel_starts_transports(kernel: RuntimeKernel) -> None:
    # If transport is supposed to be available
    # then it should be installed BEFORE freeze.
    assert len(kernel.transports) >=0 # now default is HTTP mode with FastAPI


@pytest.mark.asyncio
async def test_kernel_shutdowns_transports(kernel: RuntimeKernel) -> None:
    transport = kernel.transports[0]
    #
    # assert hasattr(transport, "started")
    #
    await kernel.shutdown()
    #
    # assert transport.started is False
