from __future__ import annotations

from dataclasses import dataclass

from .messages import Message


@dataclass(slots=True)
class Query(Message):
    """Base application query."""
