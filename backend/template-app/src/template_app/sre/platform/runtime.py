"""
Platform runtime container.

This module defines the top-level runtime composition root.
"""

from __future__ import annotations

from dataclasses import dataclass

from template_app.platform.events.bus import RuntimeEventBus
from template_app.platform.reconciliation.reconcile_loop import (
    ReconciliationLoop,
)
from template_app.platform.state_engine.engine import (
    RuntimeStateEngine,
)
from template_app.platform.state_engine.state_store import (
    RuntimeStateStore,
)


@dataclass(slots=True)
class PlatformRuntime:
    """
    Runtime platform container.

    Holds all major runtime orchestration components.
    """

    event_bus: RuntimeEventBus

    state_store: RuntimeStateStore

    state_engine: RuntimeStateEngine

    reconciliation_loop: ReconciliationLoop
