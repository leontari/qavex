from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared runtime execution context for dependency-aware health runs.

    This is what turns your system from:
        "run checks"
    into:
        "orchestrate runtime graph execution"
    """

    results: dict[str, Any] = field(default_factory=dict)

    skipped: set[str] = field(default_factory=set)

    failed: set[str] = field(default_factory=set)
