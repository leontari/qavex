import pytest

from tests.factories.kernel import build_kernel_no_transport
from tests.fakes.transports import FakeTransport


@pytest.mark.asyncio
async def test_transport_startup_called() -> None:
    kernel = build_kernel_no_transport()

    transport = FakeTransport()

    kernel.install_transport(transport)

    await kernel.startup()

    assert transport.started is True


@pytest.mark.asyncio
async def test_transport_shutdown_called() -> None:
    kernel = build_kernel_no_transport()

    transport = FakeTransport()

    kernel.install_transport(transport)

    await kernel.startup()
    await kernel.shutdown()

    assert transport.stopped is True


@pytest.mark.asyncio
async def test_transport_shutdown_called() -> None:
    kernel = build_kernel_no_transport()

    transport = FakeTransport()

    kernel.install_transport(transport)

    await kernel.startup()
    await kernel.shutdown()

    assert transport.stopped is True
