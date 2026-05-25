from __future__ import annotations

from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_runtime_contains_infrastructure_registry() -> None:
    kernel = bootstrap_kernel()

    providers = (
        kernel._context
        .runtime
        .infrastructure_registry
        .providers
    )

    assert len(providers) >= 2
