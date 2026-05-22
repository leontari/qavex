from fastapi.routing import APIRoute

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_module_routes_registered() -> None:
    kernel = bootstrap_application()

    paths = {
        route.path
        for route in kernel.app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths
