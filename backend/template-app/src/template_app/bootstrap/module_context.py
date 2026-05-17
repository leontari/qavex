from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI

    from template_app.bootstrap.protocols import DependencyProvider
    from template_app.bootstrap.runtime.hooks import LifecycleHook
    from template_app.bootstrap.runtime.kernel import RuntimeKernel
    from template_app.infrastructure.providers.base import (
        InfrastructureProvider,
    )


@dataclass(slots=True)
class ModuleSetupContext:
    """Restricted module setup context."""

    _kernel: RuntimeKernel

    @property
    def app(self) -> FastAPI:
        app = self._kernel.context.app

        if app is None:
            msg = "FastAPI application not initialized."
            raise RuntimeError(msg)

        return app

    def register_router(self, router: APIRouter) -> None:
        self.app.include_router(router)

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        self._kernel.context.runtime.lifecycle_registry.register_startup(hook)

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        self._kernel.context.runtime.lifecycle_registry.register_shutdown(hook)

    def register_dependency(self, provider: DependencyProvider) -> None:
        self._kernel.context.runtime.container.register(provider)

    def get_provider(self, name: str) -> InfrastructureProvider:
        return self._kernel.context.runtime.infrastructure_registry.get(name)
