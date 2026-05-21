from __future__ import annotations

from enum import Enum


class ModuleCapability(str, Enum):
    ROUTER = "router"
    DEPENDENCIES = "dependencies"
    LIFECYCLE = "lifecycle"
    EVENT_BUS = "event_bus"
    INFRASTRUCTURE = "infrastructure"
    COMMAND_BUS = "command_bus"
    QUERY_BUS = "query_bus"
