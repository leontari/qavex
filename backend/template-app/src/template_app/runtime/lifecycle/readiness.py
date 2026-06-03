"""
Runtime readiness gate.

Responsibilities:
    - runtime readiness state
    - readiness synchronization
    - transport startup gating
    - lifecycle coordination
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ReadinessGate:
    """
    Runtime readiness state manager.

    Responsibilities:
        - readiness ownership
        - readiness synchronization
        - transport startup gating
        - runtime startup coordination

    Notes:
        This object is intentionally transport-agnostic.

        HTTP, Kafka, gRPC, CLI, workers and orchestrators
        should only observe readiness through this gate.

    """

    _ready: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    @property
    def is_ready(self) -> bool:
        """
        Return readiness state.

        Returns:
            True if runtime is ready.

        """
        return self._ready

    def mark_ready(self) -> None:
        """Mark runtime as ready."""
        self._ready = True

    def mark_not_ready(self) -> None:
        """Mark runtime as not ready."""
        self._ready = False

    def ensure_ready(self) -> None:
        """
        Ensure runtime is ready.

        Raises:
            RuntimeError:
                If runtime is not ready.

        """
        if not self._ready:
            msg = "Runtime is not ready."
            raise RuntimeError(msg)
