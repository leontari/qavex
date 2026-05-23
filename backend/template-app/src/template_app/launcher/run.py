"""
Application launcher.

Responsibilities:
    - start process
    - select mode
    - execute runtime
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel import RuntimeKernel


class KernelLauncher:
    def __init__(self, kernel: RuntimeKernel):
        self.kernel = kernel

    def run(self, mode: str) -> None:
        if mode == "http":
            self._run_http()
        elif mode == "kafka":
            self._run_kafka()
        elif mode == "grpc":
            self._run_grpc()
        elif mode == "cli":
            self._run_cli()

    def _run_http(self):
        app = create_fastapi_app(self.kernel)

        transport = FastAPITransport(app, self.kernel)
        self.kernel.install_transport(transport)

        import uvicorn

        uvicorn.run(app)

    def _run_kafka(self):
        self.kernel.install_transport(
            KafkaTransport(build_consumer(), self.kernel)
        )
        asyncio.run(self.kernel.startup())

    def _run_grpc(self):
        self.kernel.install_transport(GRPCTransport(build_grpc(), self.kernel))
        asyncio.run(self.kernel.startup())

    def _run_cli(self):
        self.kernel.install_transport(CLITransport(self.kernel))
        asyncio.run(self.kernel.startup())
