from __future__ import annotations

from fastapi import FastAPI

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.factory import TransportFactory
from template_app.runtime.transports.http.transport import FastAPITransport


def test_http_transport_factory_creates_http_transport() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    composition = launcher.build()

    transport = TransportFactory.create_http(composition.kernel)

    assert isinstance(transport, FastAPITransport)
    assert transport.name == "http"
    assert transport.app is not None


def test_build_http_app_returns_fastapi() -> None:
    launcher = KernelLauncher(
        LauncherConfig(
            mode=LaunchMode.HTTP,
        ),
    )

    app = launcher.build_http_app()

    assert isinstance(app, FastAPI)
