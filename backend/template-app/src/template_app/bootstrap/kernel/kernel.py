"""Application runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.bootstrap.kernel import KernelContext
from template_app.bootstrap.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.modules.manifests import ModuleManifest
    from template_app.bootstrap.runtime.state import RuntimeState


@dataclass(slots=True)
class RuntimeKernel:
    """
    Central application runtime kernel.

    Responsibilities:
        - runtime orchestration
        - lifecycle orchestration
        - transport ownership
        - installed module ownership
    """

    _context: KernelContext

    _modules: tuple[ModuleManifest, ...] = field(
        default_factory=tuple,
        init=False,
    )

    ######################
    # kernel construction
    ######################

    @classmethod
    def create(
        cls,
        runtime: RuntimeState,
        app: FastAPI,
    ) -> RuntimeKernel:
        return cls(
            _context=KernelContext(
                runtime=runtime,
                app=app,
            )
        )

    ################
    # transport API
    ################

    @property
    def app(self) -> FastAPI:
        """
        Return transport application.

        Returns:
            FastAPI instance: public ASGI transport entrypoint.

        """
        if self._context.app is None:
            msg = "FastAPI transport is not installed."
            raise RuntimeError(msg)

        return self._context.app

    ################
    # module system
    ################

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        """Return immutable list of installed modules."""
        return self._modules

    def install_modules(self, manifests: tuple[ModuleManifest, ...]) -> None:
        """Install module manifests."""
        self._modules = manifests

    ################
    # Lifecycle API
    ################

    async def startup(self) -> None:
        """Execute startup lifecycle."""
        await self._context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle."""
        await self._context.runtime.lifecycle_manager.shutdown()

    #######################
    # internal module APIs
    #######################

    def build_runtime_api(self) -> ModuleRuntimeAPI:
        """Build restricted runtime API."""

        return ModuleRuntimeAPI(
            app=self._context.app,
            container=self._context.runtime.container,
            lifecycle_registry=self._context.runtime.lifecycle_registry,
        )

    def build_infra_api(self) -> ModuleInfraAPI:
        """Build restricted infrastructure API."""

        return ModuleInfraAPI(
            registry=self._context.runtime.infrastructure_registry,
        )

    def build_mesaging_api(self) -> ModuleMessagingAPI:
        """Build restricted messaging API."""

        return ModuleMessagingAPI(
            event_bus=self._context.runtime.event_bus,
            command_bus=self._context.runtime.command_bus,
            query_bus=self._context.runtime.query_bus,
        )
