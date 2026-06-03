"""gRPC runtime entrypoint."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from template_app.runtime.transports.grpc.config import GRPCTransportConfig

if TYPE_CHECKING:
    from template_app.launcher.config import LauncherConfig
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_grpc_runtime(
    kernel: RuntimeKernel,
    config: LauncherConfig,
) -> None:
    """
    Run gRPC runtime.

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
    # config = GRPCTransportConfig()

    asyncio.run(kernel.startup())
