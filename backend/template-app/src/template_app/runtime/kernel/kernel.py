"""Application runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.kernel import KernelContext
from template_app.runtime.module.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.runtime.transports.manager import TransportManager

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.runtime.kernel.state import RuntimeState
    from template_app.runtime.module.manifests import ModuleManifest
    from template_app.runtime.transports.contracts import Transport


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

    transports: TransportManager = field(default_factory=TransportManager)

    @classmethod
    def create(cls, runtime: RuntimeState) -> RuntimeKernel:
        return cls(_context=KernelContext(runtime=runtime, app=None))

    ################
    # transport API
    ################

    def attach_http_app(self, app: FastAPI) -> None:
        self._context = KernelContext(runtime=self._context.runtime, app=app)

    @property
    def app(self) -> FastAPI:
        """
        Return transport application.

        Returns:
            FastAPI instance: public ASGI transport entrypoint.

        """
        if self._context.app is None:
            msg = "No HTTP transport attached"
            raise RuntimeError(msg)

        return self._context.app

    def install_transport(self, transport: Transport) -> None:
        self.transports.register(transport)

    ################
    # module system
    ################

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        """Return immutable list of installed modules."""
        return self._modules

    def install_modules(self, manifests: tuple[ModuleManifest, ...]) -> None:
        """Install module manifests."""
        # prevents mutation bugs in tests
        if self._modules:
            msg = "Modules already installed"
            raise RuntimeError(msg)

        self._modules = manifests

    ################
    # Lifecycle API
    ################

    async def startup(self) -> None:
        """Execute kernel startup lifecycle."""
        await self.transports.startup()
        await self._context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute kernel shutdown lifecycle."""
        await self.transports.shutdown()
        await self._context.runtime.lifecycle_manager.shutdown()

    #######################
    # internal module APIs
    #######################

    def build_runtime_api(self) -> ModuleRuntimeAPI:
        """Build restricted runtime API."""
        if self._context.app is None:
            msg = "Runtime API requires HTTP transport"
            raise RuntimeError(msg)

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
