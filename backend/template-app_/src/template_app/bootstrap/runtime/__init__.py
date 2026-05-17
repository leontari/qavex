"""
Application runtime lifecycle subsystem.

This package provides centralized orchestration for the complete runtime
lifecycle of the service.

The lifecycle subsystem is responsible for:

- startup orchestration
- graceful shutdown
- runtime state transitions
- infrastructure initialization
- background task management
- scheduler coordination
- dependency container management

Architecture overview:

- manager:
    High-level lifecycle orchestration entry point.

- startup:
    Runtime startup sequence.

- shutdown:
    Graceful shutdown sequence.

- registry:
    Runtime dependency/resource registry.

- state:
    Shared lifecycle state models.

- tasks:
    Async background task management.

The lifecycle layer acts as the runtime control plane for the entire
microservice and coordinates all long-lived infrastructure components.

runtime orchestration.
"""

from __future__ import annotations

from template_app.core_.lifecycle.manager import (
    LifecycleManager,
)
from template_app.core_.lifecycle.registry import (
    LifecycleRegistry,
)
from template_app.core_.lifecycle.state import (
    LifecycleStage,
    RuntimeState,
)
from template_app.core_.lifecycle.tasks import (
    BackgroundTaskManager,
)

__all__ = [
    "BackgroundTaskManager",
    "LifecycleManager",
    "LifecycleRegistry",
    "LifecycleStage",
    "RuntimeState",
]
