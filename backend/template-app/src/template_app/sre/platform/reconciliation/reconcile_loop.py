from __future__ import annotations

import asyncio

from template_app.platform.reconciliation.planner import (
    ReconciliationPlanner,
)
from template_app.platform.state_engine.state_store import (
    RuntimeStateStore,
)


class ReconciliationLoop:
    """
    Kubernetes-style reconciliation loop.

    Continuously compares current runtime truth against desired platform
    behavior and emits runtime actions.
    """

    def __init__(
        self,
        state_store: RuntimeStateStore,
        planner: ReconciliationPlanner,
    ) -> None:
        self.state_store = state_store

        self.planner = planner

        self._running = False

    async def start(self) -> None:
        """
        Start reconciliation loop.
        """
        self._running = True

        while self._running:
            snapshot = self.state_store.get_snapshot()

            if snapshot is not None:
                actions = self.planner.plan(snapshot)

                for action in actions:
                    print(
                        f"Reconciliation action: {action}",
                    )

            await asyncio.sleep(5)

    async def stop(self) -> None:
        """
        Stop reconciliation loop.
        """
        self._running = False
