from fastapi.routing import APIRoute

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_module_routes_registered() -> None:
    kernel = bootstrap_kernel()

    paths = {
        route.path
        for route in kernel.app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths
