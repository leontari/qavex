from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)
from template_app.bootstrap.runtime.manager import (
    LifecycleManager,
)
from template_app.bootstrap.runtime.registry import (
    LifecycleRegistry,
)


def test_runtime_state_initialized() -> None:
    context = bootstrap_application()

    assert isinstance(
        context.app.state.lifecycle_registry,
        LifecycleRegistry,
    )

    assert isinstance(
        context.app.state.lifecycle_manager,
        LifecycleManager,
    )
