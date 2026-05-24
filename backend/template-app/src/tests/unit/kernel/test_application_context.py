from dataclasses import FrozenInstanceError

import pytest

from template_app.runtime.kernel.context import (
    KernelContext,
)
from tests.factories.runtime import (
    build_runtime_state,
)


def test_kernel_context_initial_state() -> None:

    runtime = build_runtime_state()

    context = KernelContext(
        runtime=runtime,
    )

    assert context.runtime is runtime


def test_kernel_context_is_immutable() -> None:

    context = KernelContext(
        runtime=build_runtime_state(),
    )

    with pytest.raises(FrozenInstanceError):

        context.runtime = build_runtime_state()  # type: ignore[misc]
