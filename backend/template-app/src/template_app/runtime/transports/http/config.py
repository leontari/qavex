"""Launcher configuration."""

from __future__ import annotations

from dataclasses import dataclass

from template_app.launcher.modes import LaunchMode


@dataclass(frozen=True, slots=True)
class HTTPTransportConfig:
    """
    Uvicorn server runtime configuration.

    Responsibilities:
        - ASGI runtime configuration
        - uvicorn configuration
        - HTTP server tuning

    Attributes:
        mode:
            Runtime launch mode.

        host:
            Bind host.

        port:
            Bind port.

        reload:
            Enable development reload.

        workers:
            Number of runtime workers.

    """

    mode: LaunchMode = LaunchMode.HTTP

    host: str = "127.0.0.1"

    port: int = 8000

    reload: bool = False

    workers: int = 1
