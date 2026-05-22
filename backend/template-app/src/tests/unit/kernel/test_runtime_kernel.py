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

    kernel = RuntimeKernel.create(
        runtime=context.runtime,
        app=context.app,
    )

    assert kernel.app is app


def test_kernel_contains_runtime() -> None:
    app = FastAPI()

    runtime = build_runtime_state()

    context = KernelContext(
        runtime=runtime,
        app=app,
    )

    kernel = RuntimeKernel.create(
        runtime=context.runtime,
        app=context.app,
    )

    assert kernel._context.runtime is runtime


def test_kernel_has_no_modules_initially() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
        app=FastAPI(),
    )

    assert kernel.modules == ()
