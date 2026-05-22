"""Application runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.kernel import KernelContext
    from template_app.bootstrap.modules.manifests import ModuleManifest


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

    context: KernelContext

    modules: tuple[ModuleManifest, ...] = field(default_factory=tuple)

    @property
    def app(self) -> FastAPI:
        """
        Return transport application.

        Returns:
            FastAPI instance: public ASGI transport entrypoint.

        """
        if self.context.app is None:
            msg = "FastAPI transport is not installed."
            raise RuntimeError(msg)

        return self.context.app

    async def startup(self) -> None:
        """Execute startup lifecycle."""
        await self.context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle."""
        await self.context.runtime.lifecycle_manager.shutdown()
