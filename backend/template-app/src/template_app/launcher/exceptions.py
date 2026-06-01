"""Launcher exceptions."""

from __future__ import annotations


class LauncherError(Exception):
    """Base launcher exception."""


class UnsupportedLaunchModeError(LauncherError):
    """Raised when unsupported launch mode is requested."""


class CompositionViolationError(LauncherError):
    """
    Raised when runtime composition rules are violated.

    Example:
        Direct kernel bootstrap outside ApplicationBuilder.

    """


class FrozenCompositionError(LauncherError):
    """Raised when composition mutation happens after freeze."""
