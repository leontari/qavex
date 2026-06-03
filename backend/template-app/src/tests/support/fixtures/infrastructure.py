from __future__ import annotations

import pytest

from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)
from template_app.runtime.kernel.kernel import RuntimeKernel


@pytest.fixture
def infrastructure_registry(kernel: RuntimeKernel) -> InfrastructureRegistry:
    """
    Return runtime infrastructure registry.
    """
    return kernel.infrastructure.registry


@pytest.fixture
def cache_provider(infrastructure_registry):
    return infrastructure_registry.cache


@pytest.fixture
def database_provider(infrastructure_registry):
    return infrastructure_registry.database


@pytest.fixture
def queue_provider(infrastructure_registry):
    return infrastructure_registry.queue
