from __future__ import annotations

from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_factory_creates_transport(kernel: RuntimeKernel) -> None:
    transport = TransportFactory.create_http(kernel=kernel)

    assert isinstance(transport, FastAPITransport)


def test_factory_install_default_transport(kernel: RuntimeKernel) -> None:
    TransportFactory.create_http(kernel=kernel)

    assert len(kernel.transports) == 1
