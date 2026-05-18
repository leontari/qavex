from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

LifecycleHandler = Callable[[], Awaitable[None]]


@dataclass(slots=True)
class LifecycleHook:
    """Lifecycle hook descriptor."""

    name: str
    handler: LifecycleHandler
