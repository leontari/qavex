"""RuntimeState."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.bootstrap.infrastructure.registry import (
        InfrastructureRegistry,
    )
    from template_app.bootstrap.kernel import Container
    from template_app.bootstrap.lifecycle.manager import LifecycleManager
    from template_app.bootstrap.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class RuntimeState:
    """Application runtime state."""

    container: Container
    lifecycle_registry: LifecycleRegistry
    lifecycle_manager: LifecycleManager
    infrastructure_registry: InfrastructureRegistry
