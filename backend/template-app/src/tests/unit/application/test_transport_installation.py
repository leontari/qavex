from __future__ import annotations

from unittest.mock import Mock

from template_app.runtime.application.builder import (
    ApplicationBuilder,
)
from tests.support.fakes.transports import FakeTransport

def test_transport_installed_before_freeze() -> None:

    builder = ApplicationBuilder()

    composition = builder.create()

    builder.install_transport(composition, FakeTransport())

    builder.freeze(composition)

    transports = (
        composition.kernel.transport_manager.transports
    )

    assert len(transports) == 1


def test_transport_is_installed_after_freeze() -> None:
    builder = ApplicationBuilder()

    composition = builder.create()

    transport = TransportFactory.create_http(
        composition.kernel,
    )

    builder.install_transport(
        composition,
        transport,
    )

    builder.freeze(composition)

    transports = composition.kernel.transports

    assert len(transports) == 1
