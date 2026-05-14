from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC
from datetime import datetime
from typing import Any
from uuid import uuid4

from template_app.platform.events.event_types import RuntimeEventType


@dataclass(slots=True)
class RuntimeEvent:
    """Runtime platform event."""

    type: RuntimeEventType

    source: str

    payload: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    event_id: str = field(
        default_factory=lambda: str(uuid4()),
    )
