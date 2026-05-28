"""Lifecycle runtime domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.manager import LifecycleManager
    from template_app.runtime.lifecycle.readiness import ReadinessGate
    from template_app.runtime.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class LifecycleRuntime:
    """
    Lifecycle runtime domain.

    Responsibilities:
        - lifecycle registry ownership
        - lifecycle orchestration ownership
        - readiness ownership
    """

    registry: LifecycleRegistry

    manager: LifecycleManager

    readiness: ReadinessGate
