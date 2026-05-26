"""
Runtime kernel.

* transport startup ONLY after lifecycle ready
* Kafka/gRPC wait for readiness automatically
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from template_app.runtime.kernel import KernelContext
from template_app.runtime.lifecycle import LifecycleManager, LifecycleRegistry
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
    Central runtime kernel.

    Responsibilities:
        - lifecycle orchestration
        - transport orchestration
        - runtime ownership
        - modules ownership
    """

    _context: KernelContext

    _modules: tuple[ModuleManifest, ...] = field(
        default_factory=tuple,
        init=False,
    )
    _transports: TransportManager = field(default_factory=TransportManager)
    _lifecycle: LifecycleManager = field(default_factory=LifecycleManager)
    _readiness: ReadinessGate = field(default_factory=ReadinessGate)

    _transport_manager: TransportManager = field(
        default_factory=TransportManager
    )

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
        self._transport_manager.install(transport)

    #################
    # lifecycle build
    #################

    def build_lifecycle(self) -> LifecycleManager:
        return LifecycleManager(snapshot=self._lifecycle.snapshot())

    async def startup(self) -> None:
        """
        Execute runtime startup.

        Order:
            1. lifecycle startup
            2. readiness validation
            3. transport startup
        """
        await self._context.runtime.lifecycle_manager.startup()

        await self._transport_manager.startup()

        # await self._transports.startup()
        # await self._context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute kernel shutdown lifecycle."""

        #        self.readiness.mark_not_ready()

        await self._transport_manager.shutdown()

        # executor = LifecycleExecutor(
        #     graph=self.lifecycle_registry.shutdown_graph(),
        # )

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
