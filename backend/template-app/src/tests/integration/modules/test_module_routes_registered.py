from fastapi.routing import APIRoute

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)
from template_app.runtime.transports.http.factory import (
    create_http_app,
)
from tests.support.factories.transport import (
    get_http_app,
)


def test_module_routes_registered() -> None:

    kernel = bootstrap_kernel()

    create_http_app(
        kernel,
    )

    app = get_http_app(
        kernel,
    )

    paths = {
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths
