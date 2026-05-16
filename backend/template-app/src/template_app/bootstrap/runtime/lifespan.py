from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi import FastAPI

    from template_app.bootstrap.application import ApplicationContext


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Unified application lifespan."""
    context: ApplicationContext = app.state.context

    await context.runtime.lifecycle_manager.startup()

    yield

    await context.runtime.lifecycle_manager.shutdown()
