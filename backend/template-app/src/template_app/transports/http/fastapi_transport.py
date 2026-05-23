from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.transports.http.lifespan import create_lifespan
from template_app.transports.http.transport import FastAPITransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def create_http_app(
    kernel: RuntimeKernel,
) -> FastAPI:

    app = FastAPI(
        title="template-app",
        lifespan=create_lifespan(kernel),
    )

    kernel.install_transport(
        FastAPITransport(app=app),
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
        }

    return app
