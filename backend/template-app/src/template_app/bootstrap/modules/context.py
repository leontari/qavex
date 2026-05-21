"""Restricted kernel API for the modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.bootstrap.modules.capabilities import ModuleCapability

if TYPE_CHECKING:
    from fastapi import APIRouter

    from template_app.bootstrap.contracts import (
        DependencyProvider,
        InfrastructureProvider,
    )
    from template_app.bootstrap.lifecycle import LifecycleHook
    from template_app.bootstrap.messaging.runtime.event_bus import (
        RuntimeEventBus,
    )
    from template_app.bootstrap.modules.apis import (
        ModuleInfraAPI,
        ModuleMessagingAPI,
        ModuleRuntimeAPI,
    )


@dataclass(slots=True)
class ModuleSetupContext:
    """
    A pluggable module's internal bootstrap API.

    Modules MUST NOT access RuntimeKernel directly.
    """

    runtime: ModuleRuntimeAPI
    infra: ModuleInfraAPI
    messaging: ModuleMessagingAPI
    capabilities: frozenset[ModuleCapability]

    ###############
    # internal API
    ###############

    def _require(self, capability: ModuleCapability) -> None:

        if capability not in self.capabilities:
            msg = f"Module lacks capability: {capability}"
            raise PermissionError(msg)

    ################
    # transport API
    ################

    def register_router(self, router: APIRouter) -> None:
        self._require(ModuleCapability.ROUTER)

        self.runtime.register_router(router)

    ################
    # lifecycle API
    ################

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        self._require(ModuleCapability.LIFECYCLE)

        self.runtime.register_startup_hook(hook)

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        self._require(ModuleCapability.LIFECYCLE)

        self.runtime.lifecycle_registry.register_shutdown(hook)

    ###################
    # DI container API
    ###################

    def register_dependency(self, provider: DependencyProvider) -> None:
        self._require(ModuleCapability.DEPENDENCIES)

        self.runtime.container.register(provider)

    ########################
    # infrastructure access
    ########################

    def get_provider(self, name: str) -> InfrastructureProvider:
        self._require(ModuleCapability.INFRASTRUCTURE)

        return self.infra.get_provider(name)

    ##################
    # messaging buses
    ##################
    @property
    def event_bus(self) -> RuntimeEventBus:
        self._require(ModuleCapability.EVENT_BUS)

        return self.messaging.event_bus
