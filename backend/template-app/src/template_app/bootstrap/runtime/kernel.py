from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.application import ApplicationContext


@dataclass(slots=True)
class RuntimeKernel:
    """Central application runtime kernel."""

    context: ApplicationContext

    async def startup(self) -> None:
        """Execute runtime startup lifecycle."""
        await self.context.runtime.lifecycle_manager.startup()

    async def shutdown(self) -> None:
        """Execute runtime shutdown lifecycle."""
        await self.context.runtime.lifecycle_manager.shutdown()
