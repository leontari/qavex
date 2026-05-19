from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel.context import ApplicationContext
from tests.factories.runtime import build_runtime_state


def build_context_no_app() -> ApplicationContext:
    """
    Build application context.

    Returns:
        ApplicationContext: pure runtime
    """
    return ApplicationContext(
        runtime=build_runtime_state(),
    )

def build_context():
    app = FastAPI()
    runtime=build_runtime_state()
    context = ApplicationContext(app=app, runtime=runtime)

    return context
