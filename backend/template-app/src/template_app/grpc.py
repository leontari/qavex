"""GRPC entrypoint."""

from __future__ import annotations

import asyncio

from template_app.runtime.bootstrap import bootstrap_kernel
from template_app.transports.grpc.transport import GRPCTransport


async def main() -> None:

    kernel = bootstrap_kernel()

    kernel.install_transport(
        GRPCTransport(),
    )

    await kernel.startup()


if __name__ == "__main__":
    asyncio.run(main())
