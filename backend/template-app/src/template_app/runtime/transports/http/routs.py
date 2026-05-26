"""Runtime readiness routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.runtime.kernel.kernel import RuntimeKernel


def create_runtime_router(
    kernel: RuntimeKernel,
) -> APIRouter:

    router = APIRouter()

    @router.get("/live")
    async def live() -> dict[str, str]:
        return {
            "status": "alive",
        }

    @router.get("/ready")
    async def ready() -> dict[str, str]:

        state = kernel._context.runtime.lifecycle_manager.state

        if not state.ready:
            raise HTTPException(
                status_code=503,
                detail="Runtime not ready.",
            )

        return {
            "status": "ready",
        }

    return router
