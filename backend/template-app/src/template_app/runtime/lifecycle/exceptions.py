"""Lifecycle exceptions."""

from __future__ import annotations


class LifecycleError(Exception):
    """Base lifecycle exception."""


class LifecycleCycleError(LifecycleError):
    """Raised when lifecycle DAG contains a cycle."""


class LifecycleHookExecutionError(LifecycleError):
    """Raised when lifecycle hook execution fails."""


class ReadinessProbeFailedError(LifecycleError):
    """Raised when readiness probe fails."""
