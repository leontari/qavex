from __future__ import annotations

import pytest

from template_app.runtime.transports.contracts import (
    Transport,
)


def test_transport_has_name(transport: Transport) -> None:
    """
    Transport must expose name.
    """
    assert transport.name


@pytest.mark.asyncio
async def test_transport_startup(transport: Transport) -> None:
    """
    Transport must start up safely.
    """
    await transport.startup()


@pytest.mark.asyncio
async def test_transport_shutdown(transport: Transport) -> None:
    """
    Transport must shut down safely.
    """
    await transport.shutdown()
