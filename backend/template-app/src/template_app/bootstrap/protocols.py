from __future__ import annotations

from typing import Protocol

from fastapi import FastAPI

from template_app.bootstrap.container import Container


class ModuleProtocol(Protocol):
    """
    Contract for application modules.

    Every module is responsible for registering its own:

    - routes
    - dependencies
    - event handlers
    - runtime hooks
    - background tasks

    Modules must NOT create infrastructure resources directly.
    They receive them through the application container.
    """

    def setup(
        self,
        app: FastAPI,
        container: Container,
    ) -> None:
        """Configure module inside application runtime."""
