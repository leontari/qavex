"""
Platform runtime bootstrap.

Responsible for constructing and wiring all platform components.
"""

from __future__ import annotations

from template_app.platform.events.bus import RuntimeEventBus
from template_app.platform.reconciliation.planner import (
    ReconciliationPlanner,
)
from template_app.platform.reconciliation.reconcile_loop import (
    ReconciliationLoop,
)
from template_app.platform.runtime import PlatformRuntime
from template_app.platform.state_engine.engine import (
    RuntimeStateEngine,
)
from template_app.platform.state_engine.policies import (
    RuntimeStatePolicy,
)
from template_app.platform.state_engine.state_store import (
    RuntimeStateStore,
)


def bootstrap_platform() -> PlatformRuntime:
    """
    Construct full runtime platform.

    Returns:
        PlatformRuntime:
            Fully wired runtime platform container.
    """
    event_bus = RuntimeEventBus()

    state_store = RuntimeStateStore()

    policy = RuntimeStatePolicy()

    state_engine = RuntimeStateEngine(
        state_store=state_store,
        event_bus=event_bus,
        policy=policy,
    )

    planner = ReconciliationPlanner()

    reconciliation_loop = ReconciliationLoop(
        state_store=state_store,
        planner=planner,
    )

    return PlatformRuntime(
        event_bus=event_bus,
        state_store=state_store,
        state_engine=state_engine,
        reconciliation_loop=reconciliation_loop,
    )
