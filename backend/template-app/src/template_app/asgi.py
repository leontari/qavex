"""ASGI entrypoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.runtime.bootstrap import bootstrap_kernel

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.runtime.kernel.kernel import RuntimeKernel

kernel: RuntimeKernel = bootstrap_kernel()

app: FastAPI = kernel.app


# kernel: KernelRuntime = bootstrap_kernel()
#
#
# def create_app() -> FastAPI:
#     app: FastAPI = FastAPI()
#     transport = FastApiTransport(app, kernel)
#     kernel.install_transport(transport)
#
#     return app
#
#
# app = create_app()
