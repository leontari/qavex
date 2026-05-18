from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel.context import ApplicationContext
from tests.factories.runtime import build_runtime_state


def build_application_context() -> ApplicationContext:
    """Build application context."""

    return ApplicationContext(
        app=FastAPI(),
        runtime=build_runtime_state(),
    )

build_runtime_state()
