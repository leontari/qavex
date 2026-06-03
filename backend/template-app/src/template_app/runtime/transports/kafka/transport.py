from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


class KafkaTransport:
    name = "kafka"

    def __init__(
        self,
        kernel: RuntimeKernel | None = None,
        consumer: object | None = None,
    ) -> None:
        self.consumer = consumer
        self.kernel = kernel
        self._task: asyncio.Task[None] | None = None

    async def startup(self) -> None:
        consumer = self.consumer
        kernel = self.kernel

        if consumer is None or kernel is None:
            return

        # await consumer.start()
        #
        # self._task = asyncio.create_task(self._loop())

    async def _loop(self) -> None:
        consumer = self.consumer
        kernel = self.kernel

        if consumer is None or kernel is None:
            return

        assert hasattr(consumer, "__aiter__")

        # async for msg in consumer:
        # await kernel.context.runtime.messaging_bus.dispatch(msg)

    async def shutdown(self) -> None:
        consumer = self.consumer
        kernel = self.kernel

        if consumer is None or kernel is None:
            return

        if self._task:
            self._task.cancel()

    # await consumer.stop()
