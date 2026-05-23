from __future__ import annotations

from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_provider_startup_hooks_registered() -> None:
    kernel = bootstrap_kernel()

    hooks = (
        kernel._context
        .runtime
        .lifecycle_registry
        .startup_hooks
    )

    names = {
        hook.name
        for hook in hooks
    }

    assert "database.startup" in names
    assert "cache.startup" in names
    assert "queue.startup" in names
