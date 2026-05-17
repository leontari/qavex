from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_provider_shutdown_hooks_registered() -> None:
    kernel = bootstrap_application()

    hooks = (
        kernel.context
        .runtime
        .lifecycle_registry
        .shutdown_hooks
    )

    names = {
        hook.name
        for hook in hooks
    }

    assert "database.shutdown" in names
    assert "redis.shutdown" in names
