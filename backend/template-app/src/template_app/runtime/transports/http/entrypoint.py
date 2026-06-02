"""HTTP runtime entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

import uvicorn

from template_app.runtime.transports.http.config import HTTPTransportConfig
from template_app.runtime.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_http_runtime(
    kernel: RuntimeKernel,
    config: LauncherConfig,
) -> None:
    """
    Run HTTP runtime.

    Important:
        No composition here.

    Notes:
        - FastAPI instance must already exist inside kernel.
        - NO transport installation here.
        - ONLY app execution.

    Args:
        kernel:
            Runtime kernel instance.
        config:
            HTTP runtime configuration

    """
    # Config is accepted for API consistency
    # temp solution while ConfigLoader is not implemented
    _ = config
    config = HTTPTransportConfig()

    transport = kernel.transport_manager.get(FastAPITransport)

    app: FastAPI = transport.app

    if transport is None:
        msg = "HTTP transport is not installed"
        raise RuntimeError(msg)

    uvicorn.run(
        app=app,
        host=config.host,
        port=config.port,
        reload=config.reload,
        workers=config.workers,
    )
