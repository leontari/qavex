"""CLI runtime entrypoint."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from template_app._version import __version__
from template_app.runtime.transports.cli.parser import build_cli_parser
from template_app.runtime.transports.cli.transport import CLITransport

if TYPE_CHECKING:
    from argparse import ArgumentParser

    from template_app.runtime.kernel.kernel import RuntimeKernel


logger = logging.getLogger(__name__)


def run_cli_runtime(kernel: RuntimeKernel) -> None:
    """
    Run CLI runtime.

    Responsibilities:
        - CLI parsing
        - CLI diagnostics
        - CLI transport execution

    Args:
        kernel:
            Runtime kernle instance
        config:
            interactive runtime configuration

    """
    parser: ArgumentParser = build_cli_parser()

    args = parser.parse_args()

    if args.version:
        logger.info(
            "template-app version: %s",
            __version__,
        )
        return

    transport = CLITransport(kernel)

    kernel.install_transport(transport)

    asyncio.run(
        kernel.startup(),
    )
