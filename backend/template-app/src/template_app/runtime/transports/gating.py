from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.readiness import ReadinessGate


@dataclass(slots=True)
class TransportGate:
    """Controls when transport is allowed to start."""

    readiness: ReadinessGate

    def allow_start(self) -> bool:
        return self.readiness.is_ready
