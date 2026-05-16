from __future__ import annotations

from fastapi.routing import APIRoute

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
