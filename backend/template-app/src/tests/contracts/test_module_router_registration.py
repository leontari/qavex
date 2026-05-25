from __future__ import annotations

from fastapi.routing import APIRoute
from fastapi import APIRouter

from template_app.runtime.module.capabilities import (
    ModuleCapability,
)
from tests.factories.module_context import (
    build_module_context,
)
from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_health_route_registered() -> None:

    kernel = bootstrap_kernel()

    paths = {
        route.path
        for route in kernel.app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths


def test_module_can_register_router() -> None:

    ctx = build_module_context(
        capabilities=frozenset({
            ModuleCapability.ROUTER,
        }),
    )

    router = APIRouter()

    @router.get("/test")
    async def test() -> dict[str, bool]:
        return {"ok": True}

    ctx.register_router(router)

    paths = {
        route.path
        for route in ctx.runtime.app.routes
        if isinstance(route, APIRoute)
    }

    assert "/test" in paths
