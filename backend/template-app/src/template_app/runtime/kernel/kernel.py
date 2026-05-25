"""Application runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.core_.app_.factory import lifecycle
from template_app.runtime.kernel import KernelContext
from template_app.runtime.lifecycle import LifecycleManager
from template_app.runtime.lifecycle.readiness import ReadinessGate
from template_app.runtime.module.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)
from template_app.runtime.transports.manager import TransportManager

if TYPE_CHECKING:
    from template_app.runtime.kernel.state import RuntimeState
    from template_app.runtime.module.manifests import ModuleManifest
    from template_app.runtime.transports.contracts import Transport


@dataclass(slots=True)
class RuntimeKernel:
    """
    Runtime kernel of the application.

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
    _transports: TransportManager = field(default_factory=TransportManager)
    _lifecycle: LifecycleManager = field(default_factory=LifecycleManager)
    _readiness: ReadinessGate = field(default_factory=ReadinessGate)

    ########
    # kernel
    ########

    @classmethod
    def create(cls, runtime: RuntimeState) -> RuntimeKernel:
        """Create immutable composition graph of the application kernel."""
        return cls(_context=KernelContext(runtime=runtime))

    @property
    def context(self) -> KernelContext:
        """Return immutable composition graph of the application kernel."""
        return self._context

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        """Return immutable list of installed modules."""
        return self._modules

    @property
    def transports(self) -> tuple[Transport, ...]:
        """Return immutable list of installed transports."""
        return self._transports.transports

    @property
    def transport_manager(self) -> TransportManager:
        """Return transport runtime manager."""
        return self._transports

    ###############
    # installations
    ###############

    def install_modules(self, manifests: tuple[ModuleManifest, ...]) -> None:
        """Install module manifests."""
        # prevents mutation bugs in tests
        if self._modules:
            msg = "Modules already installed"
            raise RuntimeError(msg)

        self._modules = manifests

    def install_transport(self, transport: Transport) -> None:
        """Install transport."""
        self._transports.install(transport)

    #################
    # lifecycle build
    #################

    def build_lifecycle(self) -> LifecycleManager:
        return LifecycleManager(snapshot=self._lifecycle.snapshot())

    async def startup(self) -> None:
        """Execute kernel startup lifecycle."""
        lifecycle = self.build_lifecycle()

        await _lifecycle.startup()

        self.readiness.mark_ready()

        await self._transports.startup()

        # await self._transports.startup()
        # await self._context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute kernel shutdown lifecycle."""
        await self._transports.shutdown()
        await self._context.runtime.lifecycle_manager.shutdown()

    #####################
    # create module APIs
    #####################

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

    def build_messaging_api(self) -> ModuleMessagingAPI:
        """Build restricted messaging API."""

        return ModuleMessagingAPI(
            event_bus=self._context.runtime.event_bus,
            command_bus=self._context.runtime.command_bus,
            query_bus=self._context.runtime.query_bus,
        )
