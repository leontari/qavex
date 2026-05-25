from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from template_app.runtime.lifecycle.hooks import LifecycleHook
from template_app.runtime.lifecycle.snapshot import LifecycleRegistrySnapshot


@dataclass(slots=True)
class LifecycleRegistry:
    """Application lifecycle hooks registry (state only)."""

    _startup_hooks: list[LifecycleHook] = field(default_factory=list)
    _shutdown_hooks: list[LifecycleHook] = field(default_factory=list)

    def register_startup(self, hook: LifecycleHook) -> None:
        """Append startup hook."""
        self._startup_hooks.append(hook)

    def register_shutdown(self, hook: LifecycleHook) -> None:
        """Append shutdown hook."""
        self._shutdown_hooks.append(hook)

    def extend_startup(self, hooks: Iterable[LifecycleHook]) -> None:
        """Extend list of startup hooks."""
        self._startup_hooks.extend(hooks)

    def extend_shutdown(self, hooks: Iterable[LifecycleHook]) -> None:
        """Extend list of startup hooks."""
        self._startup_hooks.extend(hooks)

    def snapshot(self) -> LifecycleRegistrySnapshot:
        return LifecycleRegistrySnapshot(
            startup=tuple(self._startup_hooks),
            shutdown=tuple(self._shutdown_hooks),
        )
