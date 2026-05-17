from collections.abc import Iterable
from dataclasses import dataclass, field

from template_app.bootstrap.lifecycle.hooks import LifecycleHook


@dataclass(slots=True)
class LifecycleRegistry:
    """
    Application lifecycle hooks registry.

    Stores startup and shutdown hooks registered by:

    - modules
    - infrastructure adapters
    - observability
    - runtime services
    """

    _startup_hooks: list[LifecycleHook] = field(default_factory=list)
    _shutdown_hooks: list[LifecycleHook] = field(default_factory=list)

    def register_startup(self, hook: LifecycleHook) -> None:
        """Register startup hook."""
        self._startup_hooks.append(hook)

    def register_shutdown(self, hook: LifecycleHook) -> None:
        """Register shutdown hook."""
        self._shutdown_hooks.append(hook)

    # TODO: recheck this
    def extend_startup(self, hooks: Iterable[LifecycleHook]) -> None:
        self._startup_hooks.extend(hooks)

    # TODO: recheck this
    def extend_shutdown(self, hooks: Iterable[LifecycleHook]) -> None:
        self._shutdown_hooks.extend(hooks)

    @property
    def startup_hooks(self) -> tuple[LifecycleHook, ...]:
        """Immutable startup hooks snapshot."""
        return tuple(self._startup_hooks)

    @property
    def shutdown_hooks(self) -> tuple[LifecycleHook, ...]:
        """Immutable shutdown hooks snapshot."""
        return tuple(self._shutdown_hooks)
