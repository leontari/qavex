from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.messaging.registry import RuntimeHandlerRegistry

# TODO: check if it should be deleted due to busses existence.
@pytest.fixture
def messaging_registry(kernel: RuntimeKernel) -> RuntimeHandlerRegistry:
    """
    Return runtime messaging registry.
    """
    return kernel.messaging.registry


@pytest.fixture
def event_bus(kernel: RuntimeKernel):
    return kernel.messaging.event_bus


@pytest.fixture
def command_bus(kernel: RuntimeKernel):
    return kernel.messaging.command_bus


@pytest.fixture
def query_bus(kernel: RuntimeKernel):
    return kernel.messaging.query_bus
