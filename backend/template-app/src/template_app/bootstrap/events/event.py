from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(slots=True, kw_only=True)
class Event:
    """Base runtime event."""

    name: str
    event_id: str = uuid4().hex
