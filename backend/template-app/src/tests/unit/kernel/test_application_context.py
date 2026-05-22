from dataclasses import FrozenInstanceError

from fastapi import FastAPI
import pytest

from template_app.bootstrap.kernel.context import (
    KernelContext,
)
from tests.factories.runtime import (
    build_runtime_state,
)


def test_kernel_context_initial_state() -> None:

    runtime = build_runtime_state()

    app = FastAPI()

    context = KernelContext(
        runtime=runtime,
        app=app,
    )

    assert context.runtime is runtime

    assert context.app is app


def test_kernel_context_is_immutable() -> None:

    context = KernelContext(
        runtime=build_runtime_state(),
        app=FastAPI(),
    )

    with pytest.raises(FrozenInstanceError):

        context.app = FastAPI()  # type: ignore[misc]
