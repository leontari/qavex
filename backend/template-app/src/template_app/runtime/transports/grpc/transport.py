from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


class GRPCTransport:
    def __init__(self, server, kernel: RuntimeKernel):
        self.server = server
        self.kernel = kernel

    async def startup(self) -> None:
        await self.server.start()

    async def shutdown(self) -> None:
        await self.server.stop()
