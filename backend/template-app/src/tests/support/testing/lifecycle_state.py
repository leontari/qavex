from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeLifecycleState:
    """
    Runtime lifecycle state snapshot.
    """

    started: bool = False
    stopped: bool = False
