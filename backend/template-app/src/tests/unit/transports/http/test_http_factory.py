from __future__ import annotations

from fastapi import FastAPI

from template_app.launcher.facade import build_http_app
from template_app.runtime.transports.http.transport import FastAPITransport
from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_build_http_app_returns_fastapi() -> None:
    """
    HTTP facade must return FastAPI application.
    """
    app = build_http_app()

    assert isinstance(app, FastAPI)


def test_http_transport_registered_in_runtime() -> None:
    """
    HTTP runtime must register transport during composition.
    """
    kernel = KernelTestHarness().kernel

    assert len(kernel.transports) > 0

    transport = kernel.transports[0]

    assert transport.name == "http"


def test_http_transport_registered_in_runtime_() -> None:
    kernel = KernelTestHarness().kernel

    transports = [
        t
        for t in kernel.transports
        if isinstance(t, FastAPITransport)
    ]

    assert len(transports) == 1
