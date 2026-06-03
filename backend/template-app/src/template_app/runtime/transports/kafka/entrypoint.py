"""Kafka runtime entrypoint."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from template_app.runtime.transports.kafka.config import KafkaTransportConfig

if TYPE_CHECKING:
    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_kafka_runtime(
    kernel: RuntimeKernel,
    config: LauncherConfig,
) -> None:
    """
    Run Kafka runtime.

    Responsibilities:
        - runtime lifecycle execution

    Args:
        kernel:
            Runtime kernel instance.
        config:
            LauncherConfig

    """
    # Config is accepted for API consistency
    # temp solution while ConfigLoader is not implemented
    _ = config
    kafka_config = KafkaTransportConfig()

    asyncio.run(kernel.startup())
