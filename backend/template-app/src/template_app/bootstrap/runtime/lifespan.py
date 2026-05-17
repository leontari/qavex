from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi import FastAPI

    from template_app.bootstrap.runtime.kernel import RuntimeKernel


def create_lifespan(kernel: RuntimeKernel):
    """Create application lifespan closure."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await kernel.startup()

        yield

        await kernel.shutdown()

    return lifespan
