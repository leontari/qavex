"""gRPC runtime entrypoint."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from template_app.runtime.transports.grpc.transport import GRPCTransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_grpc_runtime(kernel: RuntimeKernel) -> None:
    """
    Run gRPC runtime.

    Responsibilities:
        - gRPC transport creation
        - transport installation
        - runtime lifecycle execution

    Args:
        kernel:
            Runtime kernel instance.

    """
    transport = GRPCTransport()

    kernel.install_transport(transport)

    asyncio.run(
        kernel.startup(),
    )
