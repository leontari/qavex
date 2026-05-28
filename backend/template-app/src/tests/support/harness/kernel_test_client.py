"""Main entrypoint"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any

from template_app.runtime.kernel.bootstrap import bootstrap_kernel
from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.fakes.providers import build_fake_infrastructure


@dataclass
class KernelTestClient:
    """
    Golden test harness for full runtime kernel.

    TestClient for Kernel runtime graph.
    """

    kernel: RuntimeKernel

    ##################
    # BUILD ENTRYPOINT
    ##################
    @classmethod
    def build(
        cls,
        *,
        use_fakes: bool = True,
        install_transports: bool = False,
    ) -> "KernelTestClient":

        kernel = bootstrap_kernel()

        ########################
        # Inject fakes if needed
        ########################
        if use_fakes:
            kernel.runtime.infrastructure = build_fake_infrastructure()

        # -------------------------
        # optional transport install
        # -------------------------
        if install_transports:
            kernel.install_transports()

        return cls(kernel=kernel)

    ###################
    # Lifecycle control
    ###################
    async def startup(self) -> None:
        await self.kernel.start()

    async def shutdown(self) -> None:
        await self.kernel.stop()

    ######################
    # Runtime access layer
    ######################
    @property
    def runtime(self):
        return self.kernel.runtime

    @property
    def modules(self):
        return self.kernel.runtime.modules

    @property
    def messaging(self):
        return self.kernel.runtime.messaging

    @property
    def infra(self):
        return self.kernel.runtime.infrastructure

    @property
    def container(self):
        return self.kernel.runtime.container

    ##############
    # Test helpers
    ##############
    def install_module(self, module) -> None:
        self.kernel.runtime.modules.install(module)

    def get_provider(self, name: str) -> Any:
        return self.kernel.runtime.infrastructure.registry.get(name)

    def snapshot(self) -> dict:
        return {
            "modules": len(self.kernel.runtime.modules),
            "providers": len(self.kernel.runtime.infrastructure.registry),
            "handlers": len(self.kernel.runtime.messaging.registry),
        }
