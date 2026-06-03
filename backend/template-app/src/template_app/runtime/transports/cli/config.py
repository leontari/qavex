"""CLI transport configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CLITransportConfig:
    """
    CLI transport configuration.

    Responsibilities:
        - interactive runtime configuration
        - CLI execution behavior
        - diagnostics configuration
    """

    interactive: bool = True

    enable_colors: bool = True

    verbose: bool = False
