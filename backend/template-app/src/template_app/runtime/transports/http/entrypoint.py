"""HTTP runtime entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

import uvicorn

from template_app.runtime.transports.http.config import HTTPTransportConfig
from template_app.runtime.transports.http.factory import create_http_app
from template_app.runtime.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_http_runtime(kernel: RuntimeKernel, config: LauncherConfig) -> None:
    """
    Run HTTP runtime.

    Responsibilities:
        - FastAPI creation
        - transport installation
        - uvicorn execution

    Args:
        kernel:
            Runtime kernel instance.
        config:
            HTTP runtime configuration

    """
    config = config or HTTPTransportConfig()

    app: FastAPI = create_http_app(kernel=kernel)

    transport = FastAPITransport(app=app)

    kernel.install_transport(transport)

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        reload=config.reload,
        workers=config.workers,
        # access_log=config.access_log,
    )
