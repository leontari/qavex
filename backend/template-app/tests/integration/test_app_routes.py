from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_health_route_registered() -> None:
    kernel = bootstrap_application()

    paths = {
        route.path
        for route in kernel.context.app.routes
    }

    assert "/health" in paths
