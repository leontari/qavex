"""Launcher configuration."""

from __future__ import annotations

from dataclasses import dataclass

from template_app.launcher.modes import LaunchMode


@dataclass(frozen=True, slots=True)
class LauncherConfig:
    """
    Runtime launcher configuration.

    Responsibilities:
        - runtime mode selection
        - orchestration-level configuration
    """

    mode: LaunchMode = LaunchMode.HTTP
