from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Query:
    """Base application query."""
