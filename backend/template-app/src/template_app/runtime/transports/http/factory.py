from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.runtime.transports.http.lifespan import create_lifespan
from template_app.runtime.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def _configure_http_routes(app: FastAPI) -> None:
    """Configure builtin http transport routes."""

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
        }


def create_http_app(kernel: RuntimeKernel) -> FastAPI:
    """
    Create and install FastAPI transport.

    Responsibilities:
        - create FastAPI app
        - bind kernel lifespan
        - install HTTP transport
        - configure transport routes

    Returns:
        FastAPI:
            configured ASGI application

    """
    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(kernel),
    )

    transport = FastAPITransport(app=app)

    kernel.install_transport(transport=transport)

    _configure_http_routes(app)

    return app
