from __future__ import annotations

from template_app.platform.state_engine.snapshots import RuntimeSnapshot


class RuntimeStateStore:
    """
    Central runtime truth store.

    This is the single source of truth for:

    - readiness
    - runtime health
    - degradation state
    - reconciliation state
    """

    def __init__(self) -> None:
        self._snapshot: RuntimeSnapshot | None = None

    def set_snapshot(
        self,
        snapshot: RuntimeSnapshot,
    ) -> None:
        """
        Persist latest runtime snapshot.
        """
        self._snapshot = snapshot

    def get_snapshot(self) -> RuntimeSnapshot | None:
        """
        Return current runtime snapshot.
        """
        return self._snapshot
