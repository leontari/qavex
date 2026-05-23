from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.runtime.messaging.contracts.commands import Command
    from template_app.runtime.messaging.contracts.events import Event
    from template_app.runtime.messaging.contracts.queries import Query


@dataclass(slots=True)
class RuntimeHandlerRegistry:
    """Runtime handler registry."""

    _event_handlers: dict[type[Event], list[Any]] = field(
        default_factory=lambda: defaultdict(list),
    )

    _command_handlers: dict[type[Command], Any] = field(
        default_factory=dict,
    )

    _query_handlers: dict[type[Query], Any] = field(
        default_factory=dict,
    )

    def register_event_handler(
        self,
        event_type: type[Event],
        handler: Any,
    ) -> None:
        self._event_handlers[event_type].append(handler)

    def register_command_handler(
        self,
        command_type: type[Command],
        handler: Any,
    ) -> None:
        self._command_handlers[command_type] = handler

    def register_query_handler(
        self,
        query_type: type[Query],
        handler: Any,
    ) -> None:
        self._query_handlers[query_type] = handler

    def get_event_handlers(
        self,
        event_type: type[Event],
    ) -> tuple[Any, ...]:
        return tuple(self._event_handlers[event_type])

    def get_command_handler(
        self,
        command_type: type[Command],
    ) -> Any:
        return self._command_handlers[command_type]

    def get_query_handler(
        self,
        query_type: type[Query],
    ) -> Any:
        return self._query_handlers[query_type]
