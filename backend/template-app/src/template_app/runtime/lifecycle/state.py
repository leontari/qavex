"""Lifecycle runtime state."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LifecycleState:
    """
    Runtime lifecycle state.

    Responsibilities:
        - startup state
        - readiness state
        - shutdown state
    """

    started: bool = False
    ready: bool = False
    failed: bool = False

    executed_hooks: set[str] = field(
        default_factory=set,
    )

    failed_hooks: set[str] = field(
        default_factory=set,
    )
