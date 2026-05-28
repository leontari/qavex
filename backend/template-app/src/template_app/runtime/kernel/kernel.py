"""Runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from template_app.runtime.kernel.context import KernelContext
from template_app.runtime.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)

if TYPE_CHECKING:
    from template_app.runtime.infrastructure.runtime import (
        InfrastructureRuntime,
    )
    from template_app.runtime.kernel.state import RuntimeState
    from template_app.runtime.lifecycle.runtime import LifecycleRuntime
    from template_app.runtime.messaging.runtime import MessagingRuntime
    from template_app.runtime.modules.manifests import ModuleManifest
    from template_app.runtime.modules.runtime import ModuleRuntime
    from template_app.runtime.transports.contracts import Transport
    from template_app.runtime.transports.manager import TransportManager
    from template_app.runtime.transports.runtime import TransportRuntime


@dataclass(slots=True)
class RuntimeKernel:
    """
    Central runtime orchestration kernel.

    Responsibilities:
        - runtime orchestration
        - lifecycle orchestration
        - transport orchestration
        - startup orchestration
        - shutdown orchestration
        - runtime graph ownership
        - restricted module API creation

    """

    _context: KernelContext

    ########
    # kernel
    ########

    @classmethod
    def create(cls, runtime: RuntimeState) -> RuntimeKernel:
        """
        Create runtime kernel.

        Args:
            runtime:
                Runtime composition graph.

        Returns:
            Initialized runtime kernel.

        """
        return cls(
            _context=KernelContext(
                runtime=runtime,
            ),
        )

    ##################
    # runtime exposure
    ##################

    @property
    def context(self) -> KernelContext:
        """
        Return immutable runtime context.

        Returns:
            Immutable runtime composition graph.

        """
        return self._context

    @property
    def runtime(self) -> RuntimeState:
        """
        Return runtime composition graph.

        Returns:
            Runtime composition graph.

        """
        return self._context.runtime

    #################
    # runtime domains
    #################

    @property
    def lifecycle(self) -> LifecycleRuntime:
        """
        Return lifecycle runtime domain.

        Returns:
            Lifecycle runtime domain.

        """
        return self.runtime.lifecycle

    @property
    def infrastructure(self) -> InfrastructureRuntime:
        """
        Return infrastructure runtime domain.

        Returns:
            Infrastructure runtime domain.

        """
        return self.runtime.infrastructure

    @property
    def messaging(self) -> MessagingRuntime:
        """
        Return messaging runtime domain.

        Returns:
            Messaging runtime domain.

        """
        return self.runtime.messaging

    @property
    def transport_runtime(self) -> TransportRuntime:
        """
        Return transport runtime domain.

        Returns:
            Transport runtime domain.

        """
        return self.runtime.transports

    @property
    def module_runtime(self) -> ModuleRuntime:
        """
        Return module runtime domain.

        Returns:
            Module runtime domain.

        """
        return self.runtime.modules

    ####################
    # module information
    ####################

    @property
    def modules(self) -> tuple[ModuleManifest, ...]:
        """
        Return installed module manifests.

        Returns:
            Installed module manifests snapshot.

        """
        return self.runtime.modules.registry.modules

    #######################
    # transport information
    #######################

    @property
    def transports(self) -> tuple[Transport, ...]:
        """
        Return installed transports.

        Returns:
            Installed transports snapshot.

        """
        return self.runtime.transports.manager.transports

    @property
    def transport_manager(self) -> TransportManager:
        """
        Return transport manager.

        Returns:
            Runtime transport manager.

        """
        return self.runtime.transports.manager

    ########################
    # transport installation
    ########################

    def install_transport(self, transport: Transport) -> None:
        """
        Install runtime transport.

        Args:
            transport:
                Runtime transport.

        Raises:
            RuntimeError:
                If runtime graph frozen.

        """
        self.runtime.freeze.ensure_mutable()

        self.runtime.transports.manager.install(
            transport,
        )

    #########################
    # runtime lifecycle phase
    #########################

    async def startup(self) -> None:
        """
        Execute runtime startup sequence.

        Startup order:
            1. lifecycle startup
            2. readiness validation
            3. transport startup

        """
        await self.runtime.lifecycle.manager.startup()

        await self.runtime.transports.manager.startup()

    async def shutdown(self) -> None:
        """
        Execute runtime shutdown sequence.

        Shutdown order:
            1. transport shutdown
            2. lifecycle shutdown

        """
        await self.runtime.transports.manager.shutdown()

        await self.runtime.lifecycle.manager.shutdown()

    #####################
    # restricted APIs API
    #####################

    def create_runtime_api(self) -> ModuleRuntimeAPI:
        """
        Create restricted runtime API.

        Returns:
            Restricted runtime API.

        """
        return ModuleRuntimeAPI(
            container=self.runtime.container,
            lifecycle_registry=self.runtime.lifecycle.registry,
        )

    def create_infra_api(self) -> ModuleInfraAPI:
        """
        Create restricted infrastructure API.

        Returns:
            Restricted infrastructure API.

        """
        return ModuleInfraAPI(
            registry=self.runtime.infrastructure.registry,
        )

    def create_messaging_api(self) -> ModuleMessagingAPI:
        """
        Create restricted messaging API.

        Returns:
            Restricted messaging API.

        """
        return ModuleMessagingAPI(
            event_bus=self.runtime.messaging.event_bus,
            command_bus=self.runtime.messaging.command_bus,
            query_bus=self.runtime.messaging.query_bus,
        )
