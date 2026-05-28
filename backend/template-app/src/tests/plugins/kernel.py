from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import (
    RuntimeKernel,
)

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)

from template_app.runtime.kernel.runtime.state import (
    RuntimeState,
)


@pytest.fixture
def kernel(
    runtime_state: RuntimeState,
) -> RuntimeKernel:
    return RuntimeKernel.create(
        runtime=runtime_state,
    )


@pytest.fixture
def bootstrapped_kernel() -> RuntimeKernel:
    return bootstrap_kernel()
