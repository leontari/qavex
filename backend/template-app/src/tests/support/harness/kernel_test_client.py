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

from template_app.runtime.kernel.context import RuntimeState
from template_app.runtime.kernel.bootstrap import bootstrap_kernel
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.contracts import Transport

TTransport = TypeVar("TTransport", bound=Transport)


class KernelTestHarness:
    """
    Single runtime-aware test entrypoint.

    THIS IS THE ONLY WAT TO CREATE KERNEL IN TESTS.

    Responsibilities:
        - kernel bootstrap
        - runtime overrides
        - transport installation
        - lifecycle startup/shutdown
        - fake injection
        - transport lookup
        - runtime introspection
        - async orchestration

    """

    def __init__(self) -> None:
        self._kernel = bootstrap_kernel()

    ###############
    # kernel access
    ###############

    @property
    def kernel(self) -> RuntimeKernel:
        """Return runtime kernel."""
        return self._kernel

    @property
    def runtime(self) -> RuntimeState:
        """Return runtime graph."""
        return self._kernel.runtime

    ############
    # transports
    ############

    def install_transport(
        self,
        transport: Transport,
    ) -> None:
        """
        Inject transport without binding to execution model.

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
        """
        for transport in self.kernel.transports:
            if isinstance(
                transport,
                transport_type,
            ):
                return transport

        return None

    #####################
    # lifecycle execution
    #####################

    async def startup(self) -> None:
        """Execute runtime startup."""
        await self._kernel.startup()

    async def shutdown(self) -> None:
        """Execute runtime shutdown."""
        await self._kernel.shutdown()
