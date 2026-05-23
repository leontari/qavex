from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.infrastructure.contracts import (
        InfrastructureProvider,
    )
    from template_app.runtime.infrastructure.registry import (
        InfrastructureRegistry,
    )


@dataclass(slots=True)
class ModuleInfraAPI:
    """Restricted infrastructure access API."""

    registry: InfrastructureRegistry

    def get_provider(self, name: str) -> InfrastructureProvider:
        return self.registry.get(name)
