from __future__ import annotations

from dataclasses import dataclass

from template_app.runtime.lifecycle.hooks import LifecycleHook


@dataclass(slots=True)
class LifecycleGraph:
    """Immutable lifecycle dependency graph."""

    hooks: tuple[LifecycleHook, ...]

    def get_hook(self, name: str) -> LifecycleHook:
        for hook in self.hooks:
            if hook.name == name:
                return hook

        raise LookupError(name)
