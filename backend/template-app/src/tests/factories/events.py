from __future__ import annotations

from template_app.bootstrap.events.bus import EventBus
from template_app.bootstrap.events.dispatcher import EventDispatcher
from template_app.bootstrap.events.registry import EventRegistry


def build_event_registry() -> EventRegistry:
    """Build event registry."""

    return EventRegistry()


def build_event_dispatcher() -> EventDispatcher:
    """Build event dispatcher."""

    registry = build_event_registry()

    return EventDispatcher(registry=registry)


def build_event_bus() -> EventBus:
    """Build event bus."""

    registry = build_event_registry()

    dispatcher = EventDispatcher(registry=registry)

    return EventBus(registry=registry, dispatcher=dispatcher)
