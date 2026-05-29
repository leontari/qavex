from __future__ import annotations

import pytest

from template_app.runtime.infrastructure.registry import InfrastructureRegistry
from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.fixture
def infrastructure(kernel_harness: KernelTestHarness) -> InfrastructureRuntime:
    """
    Infrastructure runtime domain.
    """
    return kernel_harness.infrastructure


@pytest.fixture
def infrastructure_registry(
    infrastructure: InfrastructureRuntime
) -> InfrastructureRegistry:
    """
    Return infrastructure registry.
    """
    return infrastructure.registry
