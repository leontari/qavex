from __future__ import annotations

from typing import runtime_checkable

import pytest

from template_app.runtime.transports.contracts import (
    Transport,
)
from tests.support.fakes.transports import (
    FakeTransport,
)


def test_transport_contract(transport: Transport) -> None:
    """
    Transport must satisfy protocol.
    """
    assert transport.name


@pytest.mark.asyncio
async def test_transport_startup(transport: Transport) -> None:
    await transport.startup()


@pytest.mark.asyncio
async def test_transport_shutdown(transport: Transport) -> None:
    await transport.shutdown()


def test_fake_transport_satisfies_protocol() -> None:
    """
    Fake transport must satisfy runtime contract.
    """
    transport = FakeTransport(
        name="fake",
    )

    assert isinstance(
        transport,
        Transport,
    )


def test_transport_contract_runtime_checkable() -> None:
    """
    Transport contract must support isinstance().
    """
    assert runtime_checkable is not None
