from __future__ import annotations

from template_app.runtime.bootstrap import bootstrap_kernel


def test_modules_loaded_into_application() -> None:
    kernel = bootstrap_kernel()

    paths = {
        route.path
        for route in kernel.app.routes
        if hasattr(route, "path")
    }

    assert "/health" in paths
    assert "/runtime" in paths
