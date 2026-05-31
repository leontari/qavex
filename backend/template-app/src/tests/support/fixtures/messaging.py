from __future__ import annotations

import pytest

from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)
from tests.support.harness.kernel_test_harness import KernelTestHarness

# TODO: check if it should be deleted due to busses existence.
@pytest.fixture
def messaging_registry(kernel: KernelTestHarness) -> RuntimeHandlerRegistry:
    """
    Return runtime messaging registry.
    """
    return kernel.messaging.registry


@pytest.fixture
def event_bus(kernel: KernelTestHarness):
    return kernel.messaging.event_bus


@pytest.fixture
def command_bus(kernel: KernelTestHarness):
    return kernel.messaging.command_bus


@pytest.fixture
def query_bus(kernel: KernelTestHarness):
    return kernel.messaging.query_bus
