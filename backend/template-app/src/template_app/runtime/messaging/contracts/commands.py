from __future__ import annotations

from dataclasses import dataclass

from .messages import Message


@dataclass(slots=True)
class Command(Message):
    """Base application command."""
