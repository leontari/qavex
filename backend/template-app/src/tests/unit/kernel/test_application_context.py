from __future__ import annotations

from tests.factories.runtime import build_runtime_state
from template_app.bootstrap.kernel import Container
from template_app.bootstrap.kernel import ApplicationContext
from template_app.bootstrap.lifecycle import LifecycleManager
from template_app.bootstrap.lifecycle import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.bootstrap.infrastructure.registry import (
    InfrastructureRegistry,
)


def test_application_context_initial_state() -> None:
    runtime = build_runtime_state()

    context = ApplicationContext(runtime=runtime)

    assert context.app is None
    assert context.runtime is runtime
