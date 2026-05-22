"""ASGI entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.transport.http.fastapi_transport import (
    FastApiTransport,
)

# from template_app.bootstrap.runtime.bootstrap import bootstrap_application
#
# if TYPE_CHECKING:
#     from fastapi import FastAPI
#
#     from template_app.bootstrap.kernel.kernel import RuntimeKernel
#
# kernel: RuntimeKernel = bootstrap_application()
#
# app: FastAPI = kernel.app

kernel = bootstrap()


def create_app() -> FastAPI:
    app = FastAPI()
    transport = FastApiTransport(app, kernel)
    kernel.install_transport(transport)

    return app


app = create_app()
