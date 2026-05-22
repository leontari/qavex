from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_runtime_contains_infrastructure_registry() -> None:
    kernel = bootstrap_application()

    providers = (
        kernel._context
        .runtime
        .infrastructure_registry
        .providers
    )

    assert len(providers) >= 2
