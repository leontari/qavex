from __future__ import annotations

import pytest

from template_app.runtime.messaging.registry import (
    RuntimeHandlerRegistry,
)


@pytest.fixture
def messaging_registry(
    runtime,
) -> RuntimeHandlerRegistry:
    """
    Return runtime messaging registry.
    """
    return runtime.messaging.registry


@pytest.fixture
def event_bus(runtime):
    return runtime.messaging.event_bus


@pytest.fixture
def command_bus(runtime):
    return runtime.messaging.command_bus


@pytest.fixture
def query_bus(runtime):
    return runtime.messaging.query_bus
