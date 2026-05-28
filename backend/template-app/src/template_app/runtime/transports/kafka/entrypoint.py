"""Kafka runtime entrypoint."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from template_app.runtime.transports.kafka.transport import KafkaTransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_kafka_runtime(kernel: RuntimeKernel) -> None:
    """
    Run Kafka runtime.

    Responsibilities:
        - Kafka transport creation
        - transport installation
        - runtime lifecycle execution

    Args:
        kernel:
            Runtime kernel instance.

    """

    transport = KafkaTransport(
        kernel=kernel,
    )

    kernel.install_transport(transport)

    asyncio.run(
        kernel.startup(),
    )
