from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.state import RuntimeState


@pytest.fixture
def runtime_state(kernel: RuntimeKernel) -> RuntimeState:
    """
    Internal runtime graph.

    WARNING:
        Use ONLY in low-level runtime tests.
    """
    return kernel.runtime
