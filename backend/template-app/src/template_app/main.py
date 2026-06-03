"""
Application main entrypoint.

Usage examples
--------------
    HTTP server:
        python -m template_app.main --mode http

    Kafka worker:
        python -m template_app.main --mode kafka

    gRPC server:
        python -m template_app.main --mode grpc

    Interactive CLI:
        python -m template_app.main --mode cli

Architecture
------------
    main.py
    ↓
    Launcher
    ↓
    ApplicationBuilder
    ↓
    Plugin Discovery
    ↓
    DI Container
    ↓
    TransportFactory
    ↓
    Freeze
    ↓
    Runtime

Rules:
-----
    - ApplicationBuilder must never be used outside launcher/.
    - bootstrap_kernel must never be used outside runtime/application/.
    - TransportFactory must never be used outside launcher/.
    - create_http_app must never be used outside runtime/transports/http/.

"""

from __future__ import annotations

from template_app.launcher.run import KernelLauncher
from template_app.runtime.transports.cli.parser import (
    parse_launcher_config,
)


def main() -> None:
    """Run the application."""
    config = parse_launcher_config()
    launcher = KernelLauncher(config)

    launcher.run()


if __name__ == "__main__":
    main()
