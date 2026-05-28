from __future__ import annotations

from template_app.runtime.modules.capabilities import (
    ModuleCapability,
)

from tests.support.factories.module_context import (
    build_module_context,
)


def test_capability_allows_router_registration() -> None:

    context = build_module_context(
        capabilities={
            ModuleCapability.ROUTER,
        },
    )

    assert (
        ModuleCapability.ROUTER
        in context.capabilities
    )


def test_capability_allows_infrastructure_access() -> None:

    context = build_module_context(
        capabilities={
            ModuleCapability.INFRASTRUCTURE,
        },
    )

    assert (
        ModuleCapability.INFRASTRUCTURE
        in context.capabilities
    )
