from __future__ import annotations

from enum import Enum


class ModuleCapability(str, Enum):
    ROUTER = "router"
    DEPENDENCIES = "dependencies"
    INFRASTRUCTURE = "infrastructure"

    LIFECYCLE = "lifecycle"

    EVENT_BUS = "event_bus"
    COMMAND_BUS = "command_bus"
    QUERY_BUS = "query_bus"
