from tests.fakes.transports import FakeTransport
from template_app.runtime.transports import TransportManager


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


from __future__ import annotations

from dataclasses import dataclass

import pytest

from template_app.runtime.transports.manager import (
    TransportManager,
)


@dataclass
class FakeTransport:

    started: bool = False

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False


@pytest.mark.asyncio
async def test_transport_manager_startup() -> None:

    manager = TransportManager()

    transport = FakeTransport()

    manager.install(transport)

    await manager.startup()

    assert transport.started is True
