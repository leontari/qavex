from __future__ import annotations

from template_app.bootstrap.events.registry import EventRegistry


async def fake_handler(event) -> None:
    return None


def test_registry_registers_handler() -> None:
    registry = EventRegistry()

    registry.subscribe(
        "user.created",
        fake_handler,
    )

    handlers = registry.get_handlers(
        "user.created",
    )

    assert len(handlers) == 1
