from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeStatePolicy:
    """
    Runtime state classification policy.
    """

    healthy_threshold: float = 0.9

    degraded_threshold: float = 0.7

    unhealthy_threshold: float = 0.4
