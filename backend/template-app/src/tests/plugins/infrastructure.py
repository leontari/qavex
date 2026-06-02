from __future__ import annotations

import pytest

from template_app.runtime.infrastructure.registry import InfrastructureRegistry
from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from template_app.runtime.kernel.kernel import RuntimeKernel


@pytest.fixture
def infrastructure(kernel: RuntimeKernel) -> InfrastructureRuntime:
    """
    Infrastructure runtime domain.
    """
    return kernel.infrastructure


@pytest.fixture
def infrastructure_registry(
    infrastructure: InfrastructureRuntime
) -> InfrastructureRegistry:
    """
    Return infrastructure registry.
    """
    return infrastructure.registry
