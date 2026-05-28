from __future__ import annotations

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_provider_shutdown_hooks_registered() -> None:
    kernel = bootstrap_kernel()

    hooks = (
        kernel._context
        .runtime
        .lifecycle_registry
        .shutdown_hooks
    )

    names = {
        hook.name
        for hook in hooks
    }

    assert "database.shutdown" in names
    assert "cache.shutdown" in names
    assert "queue.shutdown" in names
