import pytest
from tests.support.fakes.transports import FakeTransport
from template_app.runtime.transports.manager import TransportManager


def test_transport_manager_installs_transport() -> None:
    manager = TransportManager()

    transport = FakeTransport()

    manager.install(transport)

    assert transport in manager.transports


def test_transport_manager_returns_immutable_tuple() -> None:
    manager = TransportManager()

    assert isinstance(
        manager.transports,
        tuple,
    )


def test_transport_manager_get_transport() -> None:
    manager = TransportManager()

    transport = FakeTransport()

    manager.install(transport)

    resolved = manager.get(
        FakeTransport,
    )

    assert resolved is transport


@pytest.mark.asyncio
async def test_transport_manager_startup() -> None:

    manager = TransportManager()

    transport = FakeTransport()

    manager.install(transport)

    await manager.startup()

    assert transport.started is True
