from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from template_app.bootstrap.dispatching.commands.models import Command
    from template_app.bootstrap.dispatching.queries.models import Query


@dataclass(slots=True)
class MessageHandlerRegistry:
    """Application message handler registry."""

    _commands: dict[type[Command], Any] = field(
        default_factory=dict,
    )

    _queries: dict[type[Query], Any] = field(
        default_factory=dict,
    )

    def register_command(
        self,
        command_type: type[Command],
        handler: Any,
    ) -> None:
        self._commands[command_type] = handler

    def register_query(
        self,
        query_type: type[Query],
        handler: Any,
    ) -> None:
        self._queries[query_type] = handler

    def get_command_handler(
        self,
        command_type: type[Command],
    ) -> Any:
        return self._commands[command_type]

    def get_query_handler(
        self,
        query_type: type[Query],
    ) -> Any:
        return self._queries[query_type]
