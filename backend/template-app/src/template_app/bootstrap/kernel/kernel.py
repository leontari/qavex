"""Application runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.bootstrap.kernel import KernelContext


@dataclass(slots=True)
class RuntimeKernel:
    """
    Central application runtime kernel.

    RuntimeKernel is responsible for:
      - transport orchestration;
      - module orchestration;
      - infrastructure orchestration;
      - lifecycle orchestration.

    """

    context: KernelContext

    @property
    def app(self) -> FastAPI:
        """Public ASGI transport entrypoint."""
        if self.context.app is None:
            msg = "FastAPI transport is not configured."
            raise RuntimeError(msg)

        return self.context.app

    async def startup(self) -> None:
        """Execute startup lifecycle hooks."""
        await self.context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute shutdown lifecycle hooks."""
        await self.context.runtime.lifecycle_manager.shutdown()
