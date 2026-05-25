from __future__ import annotations

from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_health_route_registered() -> None:
    kernel = bootstrap_kernel()

    paths = {
        route.path
        for route in kernel._context.app.routes
    }

    assert "/health" in paths
