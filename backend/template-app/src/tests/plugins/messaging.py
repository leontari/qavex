from __future__ import annotations

import pytest

from template_app.runtime.messaging.buses import RuntimeEventBus, \
    RuntimeCommandBus, RuntimeQueryBus
from template_app.runtime.messaging.runtime import MessagingRuntime
from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.fixture
def messaging(kernel_harness: KernelTestHarness) -> MessagingRuntime:
    """
    Return messaging runtime domain.
    """
    return kernel_harness.messaging


@pytest.fixture
def event_bus(messaging: MessagingRuntime) -> RuntimeEventBus:
    return messaging.event_bus


@pytest.fixture
def command_bus(messaging: MessagingRuntime) -> RuntimeCommandBus:
    return messaging.command_bus


@pytest.fixture
def query_bus(messaging: MessagingRuntime) -> RuntimeQueryBus:
    return messaging.query_bus
