from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from template_app.runtime.modules.context import ModuleContext


class ModuleProtocol(Protocol):
    """
    Application module contract.

    Modules configure runtime capabilities.
    """

    def setup(self, context: ModuleContext) -> None:
        """Configure module."""
