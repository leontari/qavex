from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.transports.http.fastapi_transport import (
    FastAPITransport,
)
from tests.fakes.transports import (
    FakeTransport,
)


def build_test_transport() -> FakeTransport:
    """
    Build fake testing transport.

    Used for:
    - lifecycle tests
    - kernel transport tests
    - startup/shutdown tests
    """
    return FakeTransport()


def get_http_transport(
    kernel: RuntimeKernel,
) -> FastAPITransport:
    """
    Resolve installed FastAPI transport.

    Raises:
        LookupError:
            If HTTP transport is not installed.
    """

    transport: FastAPITransport | None = kernel.transport_manager.get(
        FastAPITransport,
    )

    if transport is None:
        msg = "FastAPI transport is not installed."
        raise LookupError(msg)

    return transport


def get_http_app(
    kernel: RuntimeKernel,
) -> FastAPI:
    """
    Resolve FastAPI app from installed HTTP transport.
    """

    return get_http_transport(kernel).app
