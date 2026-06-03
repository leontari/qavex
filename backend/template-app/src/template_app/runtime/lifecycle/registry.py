"""Application lifecycle registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from template_app.runtime.lifecycle.models import (
        LifecycleHook,
        ReadinessProbe,
    )


@dataclass(slots=True)
class LifecycleRegistry:
    """
    Stores lifecycle definition graph.

    Responsibilities:
        - store startup lifecycle hooks
        - store shutdown lifecycle hooks
        - store readiness probes
        - separation of startup/shutdown graph
        - immutable runtime snapshots generation

    """

    _startup_hooks: dict[str, LifecycleHook] = field(
        default_factory=dict,
    )

    _shutdown_hooks: dict[str, LifecycleHook] = field(
        default_factory=dict,
    )

    _readiness_probes: dict[str, ReadinessProbe] = field(
        default_factory=dict,
    )

    ###############
    # startup hooks
    ###############

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        """
        Register a startup lifecycle hook.

        Args:
            hook:
                Lifecycle hook instance.

        """
        self._startup_hooks[hook.name] = hook

    def register_startup_hooks(self, hooks: Iterable[LifecycleHook]) -> None:
        """
        Register multiple startup lifecycle hooks.

        Args:
            hooks:
                Iterable of lifecycle hooks.

        """
        for hook in hooks:
            self.register_startup_hook(hook)

    @property
    def startup_hooks(self) -> tuple[LifecycleHook, ...]:
        """
        Return immutable snapshot of startup hooks.

        Returns:
            Tuple containing registered startup hooks.

        """
        return tuple(self._startup_hooks.values())

    ################
    # shutdown hooks
    ################

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        """
        Register a shutdown lifecycle hook.

        Args:
            hook:
                Lifecycle hook instance.

        """
        self._shutdown_hooks[hook.name] = hook

    def register_shutdown_hooks(self, hooks: Iterable[LifecycleHook]) -> None:
        """
        Register multiple shutdown lifecycle hooks.

        Args:
            hooks:
                Iterable of lifecycle hooks.

        """
        for hook in hooks:
            self.register_shutdown_hook(hook)

    @property
    def shutdown_hooks(self) -> tuple[LifecycleHook, ...]:
        """
        Return immutable snapshot of shutdown hooks.

        Returns:
            Tuple containing registered shutdown hooks.

        """
        return tuple(self._shutdown_hooks.values())

    ##################
    # readiness probes
    ##################

    def register_readiness_probe(self, probe: ReadinessProbe) -> None:
        """
        Register readiness probe.

        Args:
            probe:
                Readiness probe instance.

        """
        self._readiness_probes[probe.name] = probe

    def register_readiness_probes(
        self, probes: Iterable[ReadinessProbe]
    ) -> None:
        """
        Register multiple readiness probes.

        Args:
            probes:
                Iterable of readiness probes.

        """
        for probe in probes:
            self.register_readiness_probe(probe)

    @property
    def readiness_probes(self) -> tuple[ReadinessProbe, ...]:
        """
        Return immutable snapshot of readiness probes.

        Returns:
            Tuple containing registered readiness probes.

        """
        return tuple(self._readiness_probes.values())
