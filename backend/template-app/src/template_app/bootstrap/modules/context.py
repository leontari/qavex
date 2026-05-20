"""Restricted kernel API for the modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI

    from template_app.bootstrap.contracts import (
        DependencyProvider,
        InfrastructureProvider,
    )
    from template_app.bootstrap.kernel import RuntimeKernel
    from template_app.bootstrap.lifecycle import LifecycleHook
    from template_app.bootstrap.messaging.runtime.event_bus import (
        RuntimeEventBus,
    )


@dataclass(slots=True)
class ModuleSetupContext:
    """
    Internal module bootstrap API.

    Modules MUST NOT access RuntimeKernel directly.
    """

    _kernel: RuntimeKernel

    ##################################
    # transport layer (internal only)
    ##################################

    @property
    def _app(self) -> FastAPI:
        return self._kernel.context.app

    def register_router(self, router: APIRouter) -> None:
        self._app.include_router(router)

    ############
    # lifecycle
    ############

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        runtime = self._kernel.context.runtime

        runtime.lifecycle_registry.register_startup(hook)

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        runtime = self._kernel.context.runtime

        runtime.lifecycle_registry.register_shutdown(hook)

    ###############
    # DI container
    ###############

    def register_dependency(self, provider: DependencyProvider) -> None:
        runtime = self._kernel.context.runtime

        runtime.container.register(provider)

    ########################
    # infrastructure access
    ########################

    def get_provider(self, name: str) -> InfrastructureProvider:
        runtime = self._kernel.context.runtime

        return runtime.infrastructure_registry.get(name)

    ############
    # messaging
    ############
    @property
    def event_bus(self) -> RuntimeEventBus:
        return self._kernel.context.runtime.event_bus
