from __future__ import annotations

from fastapi.routing import APIRoute, APIRouter

from template_app.bootstrap.modules import ModuleSetupContext
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_health_route_registered() -> None:
    kernel = bootstrap_application()

    app = kernel.context.app

    assert app is not None

    paths = {
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths


def test_module_can_register_router() -> None:
    kernel = bootstrap_application()
    ctx = ModuleSetupContext(_kernel=kernel)

    router = APIRouter()

    @router.get("/test")
    async def test():
        return {"ok": True}

    ctx.register_router(router)

    routes = {
        route.path
        for route in kernel.app.routes
        if hasattr(route, "path")
    }

    assert "/test" in routes
