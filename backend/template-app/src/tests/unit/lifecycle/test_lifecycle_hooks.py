from __future__ import annotations

from template_app.bootstrap.lifecycle.hooks import LifecycleHook


async def fake_handler() -> None:
    return None


def test_hook_initialization() -> None:
    hook = LifecycleHook(name="startup", handler=fake_handler)

    assert hook.name == "startup"
    assert hook.handler is fake_handler
