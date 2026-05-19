from __future__ import annotations

from dataclasses import dataclass

from template_app.bootstrap.messaging.contracts.messages import (
    Message,
)


@dataclass(slots=True)
class Command(Message):
    """Base application command."""
