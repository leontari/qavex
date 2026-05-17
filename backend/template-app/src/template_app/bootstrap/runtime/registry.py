from collections.abc import Iterable

from template_app.bootstrap.runtime.hooks import LifecycleHook


class LifecycleRegistry:
    """
    Unified application lifecycle registry.

    Stores startup and shutdown hooks registered by:

    - modules
    - infrastructure adapters
    - observability
    - runtime services
    """

    def __init__(self) -> None:
        self._startup_hooks: list[LifecycleHook] = []
        self._shutdown_hooks: list[LifecycleHook] = []

    def register_startup(self, hook: LifecycleHook) -> None:
        self._startup_hooks.append(hook)

    def register_shutdown(self, hook: LifecycleHook) -> None:
        self._shutdown_hooks.append(hook)

    def extend_startup(self, hooks: Iterable[LifecycleHook]) -> None:
        self._startup_hooks.extend(hooks)

    def extend_shutdown(self, hooks: Iterable[LifecycleHook]) -> None:
        self._shutdown_hooks.extend(hooks)

    @property
    def startup_hooks(self) -> tuple[LifecycleHook, ...]:
        return tuple(self._startup_hooks)

    @property
    def shutdown_hooks(self) -> tuple[LifecycleHook, ...]:
        return tuple(self._shutdown_hooks)
