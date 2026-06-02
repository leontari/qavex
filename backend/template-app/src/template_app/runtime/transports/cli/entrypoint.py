"""CLI runtime entrypoint."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from template_app._version import __version__
from template_app.launcher.config import LauncherConfig
from template_app.runtime.transports.cli.config import CLITransportConfig
from template_app.runtime.transports.cli.parser import build_cli_parser
from template_app.runtime.transports.cli.transport import CLITransport

if TYPE_CHECKING:
    from argparse import ArgumentParser

    from template_app.runtime.kernel.kernel import RuntimeKernel


logger = logging.getLogger(__name__)


def run_cli_runtime(
    kernel: RuntimeKernel,
    config: LauncherConfig,
) -> None:
    """
    Run CLI runtime.

    Responsibilities:
        - CLI parsing
        - CLI diagnostics
        - CLI transport execution

    Args:
        config:
            LauncherConfig
        kernel:
            Runtime kernle instance

    """
    # parser: ArgumentParser = build_cli_parser()
    #
    # args = parser.parse_args()
    #
    # if args.version:
    #     logger.info(
    #         "template-app version: %s",
    #         __version__,
    #     )
    #     return

    # Config is accepted for API consistency
    # temp solution while ConfigLoader is not implemented
    _ = config
    config = CLITransportConfig()

    asyncio.run(kernel.startup())
