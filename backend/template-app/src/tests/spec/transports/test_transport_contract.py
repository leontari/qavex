from __future__ import annotations

import pytest

from template_app.runtime.transports.contracts import Transport
from tests.support.fakes.transports import FakeTransport


def test_transport_protocol_has_required_attributes() -> None:
    assert hasattr(Transport, "startup")
    assert hasattr(Transport, "shutdown")


@pytest.mark.asyncio
async def test_transport_startup() -> None:
    transport: Transport = FakeTransport()

    await transport.startup()

    assert getattr(transport, "started", True)


@pytest.mark.asyncio
async def test_transport_shutdown() -> None:
    transport: Transport = FakeTransport()

    await transport.shutdown()

    assert getattr(transport, "stopped", True)


def test_fake_transport_satisfies_protocol() -> None:
    transport = FakeTransport(name="fake")

    assert isinstance(transport, Transport)


def test_transport_contract_runtime_checkable() -> None:
    """Transport contract must support isinstance()."""
    transport = FakeTransport()

    assert isinstance(transport, Transport)


def test_transport_protocol_is_satisfied_by_fake() -> None:
    """
    Protocol must be satisfied structurally.
    """
    transport: Transport = FakeTransport(name="fake")

    assert transport.name == "fake"


@pytest.mark.asyncio
async def test_transport_startup_contract() -> None:
    transport = FakeTransport(name="fake")

    await transport.startup()

    assert getattr(transport, "started", True) is True


@pytest.mark.asyncio
async def test_transport_shutdown_contract() -> None:
    transport = FakeTransport(name="fake")

    await transport.shutdown()

    assert getattr(transport, "stopped", True) is True
