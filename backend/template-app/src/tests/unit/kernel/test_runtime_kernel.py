from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel import (
    KernelContext,
    RuntimeKernel,
)
from tests.factories.runtime import build_runtime_state


def test_kernel_returns_app() -> None:
    app = FastAPI()

    context = KernelContext(
        runtime=build_runtime_state(),
        app=app,
    )

    kernel = RuntimeKernel(
        context=context,
    )

    assert kernel.app is app


def test_kernel_contains_runtime() -> None:
    app = FastAPI()

    runtime = build_runtime_state()

    context = KernelContext(
        runtime=runtime,
        app=app,
    )

    kernel = RuntimeKernel(
        context=context,
    )

    assert kernel.context.runtime is runtime
