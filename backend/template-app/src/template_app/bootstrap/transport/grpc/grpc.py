class GRPCTransport:
    def __init__(self, server, kernel: RuntimeKernel):
        self.server = server
        self.kernel = kernel

    async def startup(self) -> None:
        await self.server.start()

    async def shutdown(self) -> None:
        await self.server.stop()
