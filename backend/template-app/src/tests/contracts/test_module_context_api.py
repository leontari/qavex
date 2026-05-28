from __future__ import annotations

from template_app.runtime.modules.apis import ModuleRuntimeAPI
from tests.factories.module_context import build_module_context


def test_module_context_has_restricted_api() -> None:

    context = build_module_context()

    assert hasattr(context, "register_router")
    assert hasattr(context, "register_dependency")
    assert hasattr(context, "register_startup_hook")

    # explicit sandbox APIs
    assert hasattr(context, "runtime")
    assert hasattr(context, "infra")
    assert hasattr(context, "messaging")

    # kernel internals MUST stay hidden
    assert not hasattr(context, "_kernel")


def test_module_context_hides_kernel_internals() -> None:

    context = build_module_context()

    assert not hasattr(context, "_kernel")
    assert not hasattr(context, "context")
    assert not hasattr(context, "state")


def test_module_context_exposes_runtime_api_only() -> None:

    context = build_module_context()

    assert isinstance(
        context.runtime,
        ModuleRuntimeAPI,
    )
