"""
Restricted module bootstrap context.

Important:
---------
Module context must NEVER depend on FastAPI.
It should only use ModuleRuntimeAPI.
No transport imports allowed.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.module.capabilities import ModuleCapability

if TYPE_CHECKING:
    from fastapi import APIRouter

    from template_app.runtime.container.contracts import (
        DependencyProvider,
    )
    from template_app.runtime.infrastructure.contracts import (
        InfrastructureProvider,
    )
    from template_app.runtime.lifecycle import LifecycleHook
    from template_app.runtime.messaging.runtime.event_bus import (
        RuntimeEventBus,
    )
    from template_app.runtime.module.apis import (
        ModuleInfraAPI,
        ModuleMessagingAPI,
        ModuleRuntimeAPI,
    )


@dataclass(slots=True)
class ModuleContext:
    """
    Restricted module API sandbox.

    Modules MUST NOT access RuntimeKernel (kernel) internals directly.
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

        self.runtime.register_shutdown_hook(hook=hook)

    #################
    # dependency API
    #################

    def register_dependency(self, provider: DependencyProvider) -> None:
        self._require(ModuleCapability.DEPENDENCIES)

        self.runtime.register_dependency(provider=provider)

    ########################
    # infrastructure access
    ########################

    def get_provider(self, name: str) -> InfrastructureProvider:
        self._require(ModuleCapability.INFRASTRUCTURE)

        return self.infra.get_provider(name)

    ##################
    # messaging API
    ##################
    @property
    def event_bus(self) -> RuntimeEventBus:
        self._require(ModuleCapability.EVENT_BUS)

        return self.messaging.event_bus
