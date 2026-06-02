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
        consumer: None = None,
    ) -> None:

        self.consumer = consumer
        self.kernel = kernel
        self._task: asyncio.Task | None = None

    async def startup(self) -> None:

        if self.consumer is None:
            return

        await self.consumer.start()
        self._task = asyncio.create_task(self._loop())

    async def _loop(self):

        async for msg in self.consumer:
            await self.kernel.context.runtime.messaging_bus.dispatch(msg)

    async def shutdown(self) -> None:

        if self.consumer is None:
            return

        if self._task:
            self._task.cancel()

        await self.consumer.stop()
