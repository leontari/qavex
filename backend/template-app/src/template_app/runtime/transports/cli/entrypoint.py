"""CLI runtime entrypoint."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from template_app.runtime.transports.cli.transport import CLITransport

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def run_cli_runtime(kernel: RuntimeKernel) -> None:
    """
    Run CLI runtime.

    Responsibilities:
        - CLI transport creation
        - transport installation
        - runtime lifecycle execution

    Args:
        kernel:
            Runtime kernel instance.

    """
    transport = CLITransport()

    kernel.install_transport(transport)

    asyncio.run(
        kernel.startup(),
    )
