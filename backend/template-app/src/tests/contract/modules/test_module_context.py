from __future__ import annotations

from template_app.runtime.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)

from tests.support.factories.module_context import (
    build_module_context,
)

class TestModuleContext:

    def test_module_context_has_restricted_api() -> None:

        context = build_module_context()

        assert isinstance(
            context.runtime,
            ModuleRuntimeAPI,
        )

        assert isinstance(
            context.infra,
            ModuleInfraAPI,
        )

        assert isinstance(
            context.messaging,
            ModuleMessagingAPI,
        )


    def test_module_context_hides_kernel_internals() -> None:

        context = build_module_context()

        assert not hasattr(
            context,
            "kernel",
        )

        assert not hasattr(
            context,
            "runtime_state",
        )

        assert not hasattr(
            context,
            "container",
        )


    def test_module_context_exposes_runtime_api_only() -> None:

        context = build_module_context()

        assert hasattr(
            context,
            "runtime",
        )

        assert hasattr(
            context,
            "infra",
        )

        assert hasattr(
            context,
            "messaging",
        )

    def test_module_context_does_not_expose_fastapi() -> None:

        context = build_module_context()

        assert not hasattr(
            context,
            "app",
        )


    def test_module_context_does_not_expose_transport() -> None:

        context = build_module_context()

        assert not hasattr(
            context,
            "transport",
        )

    def test_module_context_hides_runtime() -> None:

        context = build_module_context()

        assert not hasattr(
            context,
            "_runtime",
        )

        assert not hasattr(
            context,
            "_kernel",
        )

        assert not hasattr(
            context,
            "_context",
        )

    def test_module_context_hides_runtime_internals() -> None:

        context = build_module_context()

        assert "runtime_state" not in vars(context)
        assert "kernel" not in vars(context)


    def test_module_context_contains_capabilities() -> None:

        context = build_module_context()

        assert context.capabilities


    def test_module_context_supports_router_capability() -> None:

        context = build_module_context(
            capabilities={
                ModuleCapability.ROUTER,
            },
        )

        assert (
            ModuleCapability.ROUTER
            in context.capabilities
        )
