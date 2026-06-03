"""GRPC Transport."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


class GRPCTransport:
    name = "grpc"

    def __init__(
        self,
        server: Any | None = None,
        kernel: RuntimeKernel | None = None,
    ) -> None:

        self.server = server
        self.kernel = kernel

    async def startup(self) -> None:

        if self.server is None:
            return

        await self.server.start()

    async def shutdown(self) -> None:

        if self.server is None:
            return

        await self.server.stop()
