from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_transport_factory_creates_http_transport(
    kernel: RuntimeKernel
) -> None:
    transport = TransportFactory.create_http(kernel)

    assert isinstance(transport, FastAPITransport)
    assert transport.name == "http"
    assert transport.app is not None
