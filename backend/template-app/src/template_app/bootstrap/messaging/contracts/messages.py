from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(slots=True)
class Message:
    """Base runtime message."""

    message_id: str = uuid4().hex
