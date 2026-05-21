from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_modules_loaded_into_application() -> None:
    kernel = bootstrap_application()

    paths = {
        route.path
        for route in kernel.app.routes
        if hasattr(route, "path")
    }

    assert "/health" in paths
    assert "/runtime" in paths
