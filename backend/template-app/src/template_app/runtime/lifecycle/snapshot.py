from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.hooks import LifecycleHook


Handler = Callable[[], object]


@dataclass(frozen=True, slots=True)
class LifecycleRegistrySnapshot:
    """Immutable execution snapshot of lifecycle graph."""

    startup: tuple[LifecycleHook, ...]
    shutdown: tuple[LifecycleHook, ...]
