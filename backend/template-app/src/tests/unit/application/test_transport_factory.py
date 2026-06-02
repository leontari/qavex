from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_transport_factory_creates_transport() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    transport = TransportFactory.create_http(composition.kernel)

    assert isinstance(transport, FastAPITransport)
