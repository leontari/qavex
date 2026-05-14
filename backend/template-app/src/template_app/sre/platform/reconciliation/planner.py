from __future__ import annotations

from template_app.platform.state_engine.snapshots import RuntimeSnapshot
from template_app.platform.state_engine.transitions import RuntimeStatus


class ReconciliationPlanner:
    """
    Determines runtime actions based on synthesized state.
    """

    def plan(
        self,
        snapshot: RuntimeSnapshot,
    ) -> list[str]:
        """
        Generate reconciliation actions.
        """
        actions: list[str] = []

        if snapshot.status == RuntimeStatus.UNHEALTHY:
            actions.append("mark_not_ready")

        if "redis" in snapshot.failed_services:
            actions.append("disable_cache")

        return actions
