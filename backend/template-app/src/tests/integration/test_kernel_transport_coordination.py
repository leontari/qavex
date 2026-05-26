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
