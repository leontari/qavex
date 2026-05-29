"""
Unified runtime-aware test harness.

Architecture:
-------------

RuntimeKernel
    ↓
KernelContext (IMMUTABLE boundary)
    ↓
RuntimeState (mutable runtime graph)
    ↓
domain runtimes (lifecycle / infra / messaging / modules / transports)

"""
from __future__ import annotations

from typing import TypeVar

from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from template_app.runtime.kernel.runtime.state import RuntimeState
from template_app.runtime.kernel.bootstrap import bootstrap_kernel
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.lifecycle.runtime import LifecycleRuntime
from template_app.runtime.messaging.runtime import MessagingRuntime
from template_app.runtime.modules.runtime import ModuleRuntime
from template_app.runtime.transports.contracts import Transport
from template_app.runtime.transports.runtime import TransportRuntime

TTransport = TypeVar("TTransport", bound=Transport)


class KernelTestHarness:
    """
    Unifies runtime-aware testing harness.

    Responsibilities:
        - kernel bootstrap
        - runtime overrides
        - runtime inspection
        - transport installation
        - transport resolution
        - lifecycle startup/shutdown
        - fake injection
        - transport lookup
        - runtime introspection
        - async orchestration

    This is the ONLY valid kernel creation entrypoint in tests.
    """

    def __init__(self) -> None:
        self._kernel = bootstrap_kernel()

    ########
    # kernel
    ########

    @property
    def kernel(self) -> RuntimeKernel:
        """Return runtime kernel."""
        return self._kernel

    @property
    def runtime(self) -> RuntimeState:
        """Return runtime graph."""
        return self._kernel.runtime

    #################
    # runtime domains
    #################

    @property
    def lifecycle(self) -> LifecycleRuntime:
        return self._kernel.lifecycle

    @property
    def infrastructure(self) -> InfrastructureRuntime:
        return self._kernel.infrastructure

    @property
    def messaging(self) -> MessagingRuntime:
        return self._kernel.messaging

    @property
    def modules(self) -> ModuleRuntime:
        return self._kernel.module_runtime

    @property
    def transports(self) -> TransportRuntime:
        return self._kernel.transport_runtime

    ############
    # transports
    ############

    def install_transport(self, transport: Transport) -> None:
        """
        Install runtime transport.

        Injects transport without binding to execution model.

        Args:
            transport:
                Runtime transport.
        """
        self._kernel.install_transport(transport)

    def get_transport(self,
        transport_type: type[TTransport],
    ) -> TTransport | None:
        """
        Resolve installed transport.

        Args:
            transport_type:
                Runtime transport type.

        Returns:
            Installed transport or None

        """
        return self._kernel.transport_manager.get(transport_type)

    #####################
    # lifecycle execution
    #####################

    async def startup(self) -> None:
        """
        Execute runtime startup.
        """
        await self._kernel.startup()

    async def shutdown(self) -> None:
        """Execute runtime shutdown."""
        await self._kernel.shutdown()
