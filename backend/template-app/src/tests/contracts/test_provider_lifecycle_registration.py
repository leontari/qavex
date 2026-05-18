from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_provider_startup_hooks_registered() -> None:
    kernel = bootstrap_application()

    hooks = (
        kernel.context
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
