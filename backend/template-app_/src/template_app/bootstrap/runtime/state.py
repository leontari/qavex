"""
Runtime lifecycle state models.

This module defines shared runtime state used during application startup,
shutdown, and long-running orchestration management.

The lifecycle subsystem coordinates:

- infrastructure initialization
- async background task management
- graceful shutdown orchestration
- scheduler runtime state
- dependency startup ordering
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LifecycleStage(StrEnum):
    """
    Application lifecycle stages.
    """

    INITIALIZING = "initializing"

    STARTING = "starting"

    RUNNING = "running"

    STOPPING = "stopping"

    STOPPED = "stopped"

    FAILED = "failed"


@dataclass(slots=True)
class RuntimeState:
    """
    Global runtime application state.

    Attributes:
        stage:
            Current lifecycle stage.

        resources:
            Initialized infrastructure resources.

        startup_complete:
            Indicates startup completion.

        shutdown_complete:
            Indicates graceful shutdown completion.
    """

    stage: LifecycleStage = LifecycleStage.INITIALIZING

    resources: dict[str, Any] = field(default_factory=dict)

    startup_complete: bool = False

    shutdown_complete: bool = False
