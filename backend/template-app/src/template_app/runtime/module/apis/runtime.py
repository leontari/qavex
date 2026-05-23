from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI

    from template_app.runtime.container.container import Container
    from template_app.runtime.container.contracts import (
        DependencyProvider,
    )
    from template_app.runtime.lifecycle import (
        LifecycleHook,
        LifecycleRegistry,
    )


@dataclass(slots=True)
class ModuleRuntimeAPI:
    """
    Restricted runtime API exposed to modules.

    Modules MUST NOT access RuntimeKernel directly.
    """

    app: FastAPI

    container: Container

    lifecycle_registry: LifecycleRegistry

    ################
    # transport API
    ################

    def register_router(self, router: APIRouter) -> None:
        self.app.include_router(router)

    ################
    # lifecycle API
    ################

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        self.lifecycle_registry.register_startup(hook)

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        self.lifecycle_registry.register_shutdown(hook)

    #################
    # dependency API
    #################

    def register_dependency(self, provider: DependencyProvider) -> None:
        self.container.register(provider)
