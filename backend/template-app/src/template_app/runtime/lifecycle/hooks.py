from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

LifecycleHandler = Callable[[], Awaitable[None]]


@dataclass(frozen=True, slots=True)
class LifecycleHook:
    """Lifecycle hook descriptor."""

    name: str

    handler: LifecycleHandler

    depends_on: frozenset[str] = field(default_factory=frozenset)

    retries: int = 1

    critical: bool = True
