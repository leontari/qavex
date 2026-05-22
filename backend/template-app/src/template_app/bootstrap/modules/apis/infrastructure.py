from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.contracts import (
        InfrastructureProvider,
    )
    from template_app.bootstrap.infrastructure import (
        InfrastructureRegistry,
    )


@dataclass(slots=True)
class ModuleInfraAPI:
    """Restricted infrastructure access API."""

    registry: InfrastructureRegistry

    def get_provider(self, name: str) -> InfrastructureProvider:
        return self.registry.get(name)
