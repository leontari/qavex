from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel import ApplicationContext
from tests.factories.runtime import build_runtime_state


def test_application_context_contains_runtime() -> None:
    app = FastAPI()

    context = ApplicationContext(
        runtime=build_runtime_state(),
        app=app,
    )

    assert context.runtime is not None


def test_application_context_contains_fastapi() -> None:
    app = FastAPI()

    context = ApplicationContext(
        runtime=build_runtime_state(),
        app=app,
    )

    assert context.app is app
