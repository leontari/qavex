from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder
from tests.support.fakes.transports import FakeTransport


def test_installed_transport_survives_freeze() -> None:
    transport = FakeTransport()
    builder = ApplicationBuilder()
    composition = builder.create()

    builder.install_transport(composition, transport)
    builder.freeze(composition)

    transports = composition.kernel.transports

    assert len(transports) == 1
    assert transports[0] is transport
    assert transport in transports


def test_kernel_transports_returns_tuple() -> None:
    transport = FakeTransport()
    builder = ApplicationBuilder()
    composition = builder.create()

    builder.install_transport(composition, transport)
    builder.freeze(composition)

    transports = composition.kernel.transports

    assert isinstance(transports, tuple)
