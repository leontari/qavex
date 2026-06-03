"""CLI argument parser."""

from __future__ import annotations

import argparse

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode


def build_cli_parser() -> argparse.ArgumentParser:
    """
    Build CLI parser.

    Returns:
        Configured CLI parser.

    """
    parser = argparse.ArgumentParser(
        prog="template-app",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show application version.",
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="http",
        help="Runtime launch mode.",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
    )

    parser.add_argument(
        "--reload",
        action="store_true",
    )

    return parser


def parse_launcher_config() -> LauncherConfig:
    """
    Parse launcher configuration.

    Returns:
        Parsed launcher configuration.

    """
    parser = build_cli_parser()

    args = parser.parse_args()

    return LauncherConfig(
        mode=LaunchMode.from_string(
            args.mode,
        ),
        # host=args.host,
        # port=args.port,
        # reload=args.reload,
    )
