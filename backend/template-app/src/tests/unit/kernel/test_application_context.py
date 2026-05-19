from __future__ import annotations

from tests.factories.runtime import build_runtime_state
from template_app.bootstrap.kernel import ApplicationContext
from template_app.bootstrap.runtime.state import RuntimeState


def test_application_context_initial_state() -> None:
    context = ApplicationContext(runtime=build_runtime_state())

    assert context.app is None
    assert isinstance(context.runtime, RuntimeState)
