from __future__ import annotations

from template_app.platform.events.bus import RuntimeEventBus
from template_app.platform.events.event_types import RuntimeEventType
from template_app.platform.events.models import RuntimeEvent
from template_app.platform.state_engine.policies import RuntimeStatePolicy
from template_app.platform.state_engine.snapshots import RuntimeSnapshot
from template_app.platform.state_engine.state_store import RuntimeStateStore
from template_app.platform.state_engine.transitions import RuntimeStatus


class RuntimeStateEngine:
    """
    Runtime state synthesis engine.

    Converts distributed signals into global runtime truth.
    """

    def __init__(
        self,
        state_store: RuntimeStateStore,
        event_bus: RuntimeEventBus,
        policy: RuntimeStatePolicy,
    ) -> None:
        self.state_store = state_store

        self.event_bus = event_bus

        self.policy = policy

    async def evaluate(
        self,
        score: float,
        failed: list[str],
        degraded: list[str],
    ) -> RuntimeSnapshot:
        """Compute global runtime state."""
        previous = self.state_store.get_snapshot()

        status = self._classify(score)

        snapshot = RuntimeSnapshot(
            status=status,
            score=score,
            failed_services=failed,
            degraded_services=degraded,
        )

        self.state_store.set_snapshot(snapshot)

        await self._emit_transitions(
            previous,
            snapshot,
        )

        return snapshot

    def _classify(
        self,
        score: float,
    ) -> RuntimeStatus:
        """Classify runtime status."""
        if score <= self.policy.unhealthy_threshold:
            return RuntimeStatus.UNHEALTHY

        if score <= self.policy.degraded_threshold:
            return RuntimeStatus.DEGRADED

        return RuntimeStatus.HEALTHY

    async def _emit_transitions(
        self,
        previous: RuntimeSnapshot | None,
        current: RuntimeSnapshot,
    ) -> None:
        """Emit runtime transition events."""
        if previous is None:
            return

        if previous.status != current.status:
            await self.event_bus.emit(
                RuntimeEvent(
                    type=RuntimeEventType.HEALTH_CHANGED,
                    source="runtime_state_engine",
                    payload={
                        "previous": previous.status,
                        "current": current.status,
                    },
                ),
            )

        if current.status == RuntimeStatus.DEGRADED:
            await self.event_bus.emit(
                RuntimeEvent(
                    type=RuntimeEventType.SERVICE_DEGRADED,
                    source="runtime_state_engine",
                    payload={
                        "score": current.score,
                    },
                ),
            )
