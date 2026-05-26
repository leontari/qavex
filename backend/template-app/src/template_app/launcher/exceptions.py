"""Launcher exceptions."""

from __future__ import annotations


class LauncherError(Exception):
    """Base launcher exception."""


class UnsupportedLaunchModeError(LauncherError):
    """Raised when unsupported launch mode is requested."""
