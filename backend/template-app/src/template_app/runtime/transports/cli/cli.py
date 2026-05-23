from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel import RuntimeKernel


class CLITransport:
    def __init__(self, kernel: RuntimeKernel):
        self.kernel = kernel

    async def startup(self) -> None:
        print("CLI started")
        await self._loop()

    async def _loop(self):
        while True:
            cmd = input("> ")
            if cmd == "exit":
                break
            result = await self.kernel.context.runtime.messaging.dispatch(cmd)
            print(result)

    async def shutdown(self) -> None:
        print("CLI shutdown")
