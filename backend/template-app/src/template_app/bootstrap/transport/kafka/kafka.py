class KafkaTransport:
    def __init__(self, consumer, kernel: RuntimeKernel):
        self.consumer = consumer
        self.kernel = kernel
        self._task: asyncio.Task | None = None

    async def startup(self) -> None:
        await self.consumer.start()
        self._task = asyncio.create_task(self._loop())

    async def _loop(self):
        async for msg in self.consumer:
            await self.kernel.context.runtime.messaging_bus.dispatch(msg)

    async def shutdown(self) -> None:
        if self._task:
            self._task.cancel()
        await self.consumer.stop()
