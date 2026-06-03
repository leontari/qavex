from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


class CLITransport:  # noqa: D101
    name: str = "http"

    def __init__(self, kernel: RuntimeKernel) -> None:  # noqa: ANN204, D107
        self.kernel = kernel

    async def startup(self) -> None:  # noqa: D102
        print("CLI started")  # noqa: T201
        await self._loop()

    async def _loop(self) -> None:  # noqa: ANN202
        while True:
            cmd = input("> ")  # noqa: ASYNC250

            if cmd == "exit":
                break

            # result = await self.kernel.context.runtime.messaging.dispatch(cmd)
            # print(result)  # noqa: T201

            print(f"command={cmd}")  # noqa: T201

    async def shutdown(self) -> None:  # noqa: PLR6301, D102
        print("CLI shutdown")  # noqa: T201
