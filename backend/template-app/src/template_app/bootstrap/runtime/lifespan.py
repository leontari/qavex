from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable
    from contextlib import AbstractAsyncContextManager

    from fastapi import FastAPI

    from template_app.bootstrap.kernel.kernel import RuntimeKernel


def create_lifespan(
    kernel: RuntimeKernel,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    """Build FastAPI lifespan from runtime kernel."""

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:

        await kernel.startup()

        try:
            yield

        finally:
            await kernel.shutdown()

    return lifespan
