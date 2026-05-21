from dataclasses import FrozenInstanceError

import pytest
from fastapi import FastAPI

from template_app.bootstrap.kernel.context import (
    KernelContext,
)
from tests.factories.runtime import (
    build_runtime_state,
)


def test_kernel_context_is_immutable() -> None:

    context = KernelContext(
        runtime=build_runtime_state(),
        app=FastAPI(),
    )

    with pytest.raises(FrozenInstanceError):

        context.app = FastAPI()  # type: ignore[misc]
