from __future__ import annotations

from fastapi.routing import APIRoute

from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_health_route_registered() -> None:
    kernel = bootstrap_kernel()

    app = kernel._context.app

    assert app is not None

    paths = {
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths
