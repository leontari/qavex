"""CLI runtime entrypoint."""

from __future__ import annotations

import argparse
import logging

from template_app._version import __version__
from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher
from template_app.runtime.kernel.bootstrap import bootstrap_kernel

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.

    Returns:
        Configured CLI parser.

    """
    parser = argparse.ArgumentParser(
        prog="template_app",
    )

    parser.add_argument(
        "--version", action="store_true", help="Show application version."
    )

    return parser


def main() -> None:
    """
    Run CLI runtime.

    Responsibilities:
        - CLI argument parsing
        - version rendering
        - CLI runtime startup

    """
    parser = build_parser()

    args = parser.parse_args()

    if args.version:
        logger.info(
            "template-app version: %s",
            __version__,
        )
        return

    kernel = bootstrap_kernel()

    launcher = KernelLauncher(
        _kernel=kernel,
        _config=LauncherConfig(mode=LaunchMode.CLI),
    )

    launcher.run()


if __name__ == "__main__":
    main()
