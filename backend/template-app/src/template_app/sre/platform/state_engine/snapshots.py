from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC
from datetime import datetime

from template_app.platform.state_engine.transitions import RuntimeStatus


@dataclass(slots=True)
class RuntimeSnapshot:
    """Immutable runtime state snapshot."""

    status: RuntimeStatus

    score: float

    failed_services: list[str] = field(default_factory=list)

    degraded_services: list[str] = field(default_factory=list)

    generated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
