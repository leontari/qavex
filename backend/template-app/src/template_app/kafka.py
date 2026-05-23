"""KAFKA entrypoint."""

from __future__ import annotations

import asyncio

from transports.kafka.transport import KafkaTransport

from template_app.runtime.bootstrap import bootstrap_kernel


async def main() -> None:

    kernel = bootstrap_kernel()

    kernel.install_transport(
        KafkaTransport(),
    )

    await kernel.startup()


if __name__ == "__main__":
    asyncio.run(main())
