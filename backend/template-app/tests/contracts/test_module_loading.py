from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_modules_loaded_into_application() -> None:
    context = bootstrap_application()

    paths = {
        route.path
        for route in context.app.routes
    }

    assert "/health" in paths
    assert "/runtime" in paths
