"""RuntimeState."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.container import Container
    from template_app.bootstrap.runtime.manager import LifecycleManager
    from template_app.bootstrap.runtime.registry import LifecycleRegistry
    from template_app.infrastructure.providers.registry import (
        InfrastructureRegistry,
    )


@dataclass(slots=True)
class RuntimeState:
    """Application runtime state."""

    container: Container
    lifecycle_registry: LifecycleRegistry
    lifecycle_manager: LifecycleManager
    infrastructure_registry: InfrastructureRegistry
