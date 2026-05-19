from __future__ import annotations

import pytest
from fastapi import FastAPI

from template_app.bootstrap.kernel import (
    RuntimeKernel,
    ApplicationContext,
)
from tests.factories.runtime import build_runtime_state


def test_kernel_requires_initialized_app() -> None:
    kernel = RuntimeKernel(
        context=ApplicationContext(
            runtime=build_runtime_state(),
        )
    )

    with pytest.raises(RuntimeError):
        _ = kernel.app



def test_kernel_returns_app() -> None:
    context = ApplicationContext(runtime=build_runtime_state())

    app = FastAPI()

    context.app = app

    kernel = RuntimeKernel(context=context)

    assert kernel.app is app
