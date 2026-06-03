from __future__ import annotations

import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.messaging.buses import (
    RuntimeEventBus,
    RuntimeCommandBus,
    RuntimeQueryBus,
)
from template_app.runtime.messaging.runtime import MessagingRuntime


@pytest.fixture
def messaging(kernel: RuntimeKernel) -> MessagingRuntime:
    """
    Return messaging runtime domain.
    """
    return kernel.messaging


@pytest.fixture
def event_bus(messaging: MessagingRuntime) -> RuntimeEventBus:
    return messaging.event_bus


@pytest.fixture
def command_bus(messaging: MessagingRuntime) -> RuntimeCommandBus:
    return messaging.command_bus


@pytest.fixture
def query_bus(messaging: MessagingRuntime) -> RuntimeQueryBus:
    return messaging.query_bus
