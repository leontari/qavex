"""Lifecycle manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.lifecycle.dag import LifecycleDAGExecutor
from template_app.runtime.lifecycle.exceptions import ReadinessProbeFailedError
from template_app.runtime.lifecycle.state import LifecycleState

if TYPE_CHECKING:
    from template_app.runtime.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class LifecycleManager:
    """
    Runtime lifecycle orchestration manager.

    Responsibilities:
        - startup orchestration
        - shutdown orchestration
        - readiness orchestration
        - lifecycle DAG execution
        - runtime lifecycle state management

    """

    _registry: LifecycleRegistry

    _state: LifecycleState = field(
        default_factory=LifecycleState,
    )

    _dag_executor: LifecycleDAGExecutor = field(
        default_factory=LifecycleDAGExecutor,
    )

    ##################
    # public accessors
    ##################
    @property
    def state(self) -> LifecycleState:
        """
        Return runtime lifecycle state.

        Returns:
            Current lifecycle runtime state.

        """
        return self._state

    @property
    def registry(self) -> LifecycleRegistry:
        """
        Return lifecycle registry.

        Returns:
            Registered lifecycle objects registry.

        """
        return self._registry

    ###############
    # startup phase
    ###############

    async def startup(self) -> None:
        """
        Execute application startup lifecycle.

        Responsibilities:
            - execute startup DAG
            - execute readiness probes
            - transition runtime state to ready

        """
        await self._dag_executor.execute(self.registry.startup_hooks)
        await self._execute_readiness_probes()

        self._state.started = True
        self._state.ready = True

    ################
    # shutdown phase
    ################

    async def shutdown(self) -> None:
        """
        Execute application shutdown lifecycle.

        Responsibilities:
            - execute shutdown DAG
            - transition runtime state to stopped

        """
        await self._dag_executor.execute(self.registry.shutdown_hooks)

        self._state.ready = False
        self._state.started = False

    ####################
    # readiness handling
    ####################

    async def _execute_readiness_probes(self) -> None:
        """
        Execute registered readiness probes.

        Raises:
            ReadinessProbeFailedError:
                If a critical readiness probe fails.

        """
        for probe in self._registry.readiness_probes:
            result = await probe.handler()

            if not result and probe.critical:
                msg = f"Probe failed: {probe.name}"

                raise ReadinessProbeFailedError(msg)
