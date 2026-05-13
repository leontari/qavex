"""
Application State.

Core idea:
* single source of runtime truth

"""

# core/lifecycle/state.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppState:
    db: Any | None = None
    redis: Any | None = None
    kafka: Any | None = None

    health_ready: bool = False
    startup_complete: bool = False

    background_tasks: set = field(default_factory=set)
