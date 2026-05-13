"""
Application Lifecycle Manager.

Core center manager.
"""

# core/lifecycle/manager.py
from __future__ import annotations

from fastapi import FastAPI

from template_app.core.lifecycle.shutdown import shutdown_all
from template_app.core.lifecycle.startup import startup_all
from template_app.core.lifecycle.state import AppState


class LifecycleManager:
    def __init__(self) -> None:
        self.state = AppState()

    async def startup(self, app: FastAPI) -> None:
        await startup_all(app, self.state)

    async def shutdown(self, app: FastAPI) -> None:
        await shutdown_all(app, self.state)
