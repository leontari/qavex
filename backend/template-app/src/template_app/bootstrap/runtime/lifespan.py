from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi import FastAPI

    from template_app.bootstrap.runtime.manager import LifecycleManager


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    """Unified application lifespan."""
    manager: LifecycleManager = app.state.lifecycle_manager

    await manager.startup()

    yield

    await manager.shutdown()
