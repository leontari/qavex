"""Lifecycle runtime models."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

LifecycleHandler = Callable[[], Awaitable[None]]
ReadinessHandler = Callable[[], Awaitable[bool]]


@dataclass(slots=True, frozen=True)
class RetryPolicy:
    """
    Lifecycle retry policy.

    Responsibilities:
        - retry orchestration metadata
    """

    retries: int = 0
    backoff_ms: int = 0


@dataclass(slots=True, frozen=True)
class LifecycleHook:
    """
    Runtime lifecycle hook.

    Responsibilities:
        - startup/shutdown execution unit
        - dependency graph node
        - retry + criticality control
    """

    name: str
    handler: LifecycleHandler

    dependencies: frozenset[str] = frozenset()

    critical: bool = True
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)


@dataclass(slots=True, frozen=True)
class ReadinessProbe:
    """
    Runtime readiness probe.

    Responsibilities:
        - readiness gate
        - dependency health validation
    """

    name: str
    handler: ReadinessHandler

    critical: bool = True
