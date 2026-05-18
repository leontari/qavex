from __future__ import annotations

from template_app.bootstrap.kernel.context import ApplicationContext
from template_app.bootstrap.runtime.state import RuntimeState


def test_application_context_allows_empty_app() -> None:
    runtime = RuntimeState(
        container=None,
        lifecycle_registry=None,
        lifecycle_manager=None,
        infrastructure_registry=None,
    )

    context = ApplicationContext(
        runtime=runtime,
    )

    assert context.app is None
