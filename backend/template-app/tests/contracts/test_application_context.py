from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.runtime.manager import LifecycleManager
from template_app.bootstrap.runtime.registry import LifecycleRegistry
from template_app.bootstrap.runtime.state import RuntimeState


def test_application_context_created() -> None:
    registry = LifecycleRegistry()

    runtime = RuntimeState(
        container=Container(),
        lifecycle_registry=registry,
        lifecycle_manager=LifecycleManager(
            registry=registry,
        ),
    )

    context = ApplicationContext(
        app=FastAPI(),
        runtime=runtime,
    )

    assert context.runtime is runtime
