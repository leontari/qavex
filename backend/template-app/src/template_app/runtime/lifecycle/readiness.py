from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReadinessGate:
    """Controls whether system is ready to serve traffic."""

    _ready: bool = False

    def mark_ready(self) -> None:
        self._ready = True

    def mark_not_ready(self) -> None:
        self._ready = False

    @property
    def is_ready(self) -> bool:
        return self._ready
