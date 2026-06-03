from __future__ import annotations

import pytest

from template_app.runtime.transports.manager import TransportManager

from tests.support.fakes.transports import FakeTransport


def test_transport_manager_installs_transport() -> None:
    """Transport manager should install transports."""
    manager = TransportManager()

    transport = FakeTransport(name="fake_transport")

    manager.install(transport)

    assert transport in manager.transports
    assert manager.transports == (transport,)


def test_transports_snapshot_immutable() -> None:
    """Transport snapshot should be immutable."""
    manager = TransportManager()

    manager.install(FakeTransport(name="one"))

    transports = manager.transports

    assert isinstance(transports, tuple)


def test_get_transport_by_type() -> None:
    """
    Manager should resolve transport by type.
    """
    manager = TransportManager()

    transport = FakeTransport(
        name="fake",
    )

    manager.install(
        transport,
    )

    resolved = manager.get(
        FakeTransport,
    )

    assert resolved is transport


def test_get_unknown_transport_returns_none() -> None:
    """
    Unknown transport should return None.
    """
    manager = TransportManager()

    resolved = manager.get(
        FakeTransport,
    )

    assert resolved is None


@pytest.mark.asyncio
async def test_startup_all_transports() -> None:
    """
    Manager should start up all transports.
    """
    manager = TransportManager()

    first = FakeTransport(name="first")
    second = FakeTransport(name="second")

    manager.install(first)
    manager.install(second)

    await manager.startup()

    assert first.started is True
    assert second.started is True


@pytest.mark.asyncio
async def test_shutdown_all_transports_reverse_order() -> None:
    """
    Shutdown should happen in reverse order.
    """
    events: list[str] = []

    manager = TransportManager()

    first = FakeTransport(
        name="first",
        events=events,
    )

    second = FakeTransport(
        name="second",
        events=events,
    )

    manager.install(first)
    manager.install(second)

    await manager.shutdown()

    assert events == [
        "shutdown:second",
        "shutdown:first",
    ]
