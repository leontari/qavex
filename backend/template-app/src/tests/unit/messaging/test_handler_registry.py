from __future__ import annotations

import pytest

from template_app.bootstrap.messaging.commands import Command
from template_app.bootstrap.messaging.exceptions import (
    HandlerNotRegisteredError,
)
from template_app.bootstrap.messaging.registry import (
    MessageHandlerRegistry,
)


class FakeCommand(Command):
    pass


def test_registry_raises_on_missing_handler() -> None:
    registry = MessageHandlerRegistry()

    with pytest.raises(HandlerNotRegisteredError):
        registry.get_command_handler(FakeCommand)
