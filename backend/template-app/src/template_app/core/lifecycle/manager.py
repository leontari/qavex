"""
Central runtime lifecycle manager.

This module provides the high-level orchestration layer coordinating:

- startup execution
- shutdown execution
- runtime resource registration
- application state transitions
- background task management

The lifecycle manager acts as the runtime control plane for the service.
"""

from __future__ import annotations

from fastapi import FastAPI

from template_app.core.lifecycle.registry import (
    LifecycleRegistry,
)
from template_app.core.lifecycle.shutdown import (
    shutdown,
)
from template_app.core.lifecycle.startup import (
    startup,
)
from template_app.core.lifecycle.state import (
    RuntimeState,
)
from template_app.core.lifecycle.tasks import (
    BackgroundTaskManager,
)


class LifecycleManager:
    """Runtime lifecycle orchestration manager."""

    def __init__(self) -> None:
        """Initialize lifecycle manager."""
        self.registry = LifecycleRegistry()

        self.runtime_state = RuntimeState()

        self.task_manager = BackgroundTaskManager()

    async def startup(
        self,
        app: FastAPI,
    ) -> None:
        """
        Execute application startup lifecycle.

        Args:
            app:
                FastAPI application instance.

        """
        app.state.runtime_state = self.runtime_state

        app.state.lifecycle_registry = self.registry

        app.state.task_manager = self.task_manager

        await startup(app)

    async def shutdown(
        self,
        app: FastAPI,
    ) -> None:
        """
        Execute application shutdown lifecycle.

        Args:
            app:
                FastAPI application instance.

        """
        await shutdown(app)
