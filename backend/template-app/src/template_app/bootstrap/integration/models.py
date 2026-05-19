from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IntegrationEvent:
    """Base integration event."""

    name: str
