from __future__ import annotations

from template_app.bootstrap.kernel.context import ApplicationContext
from tests.factories.runtime import build_runtime_state


def test_application_context_allows_empty_app() -> None:
    runtime = build_runtime_state()

    context = ApplicationContext(runtime=runtime)

    assert context.app is None
