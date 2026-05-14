from __future__ import annotations

from typing import Protocol

from template_app.platform.state_engine.snapshots import RuntimeSnapshot


class RuntimeAction(Protocol):
    """
    Runtime reconciliation action.
    """

    async def execute(
        self,
        snapshot: RuntimeSnapshot,
    ) -> None:
        """
        Execute reconciliation action.
        """
