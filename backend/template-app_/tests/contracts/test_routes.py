from template_app.runtime.kernel.runtime import (
    bootstrap_application,
)


def test_routes_registered():
    context = bootstrap_application()

    paths = {
        route.path
        for route in context.app.routes
    }

    assert "/health" in paths
