from tests.factories.module_context import (
    build_module_context,
)

from template_app.runtime.infrastructure import (
    CacheProvider,
)

from template_app.runtime.module.capabilities import (
    ModuleCapability,
)


def test_module_can_register_dependency() -> None:
    context = build_module_context(
        capabilities=frozenset({
            ModuleCapability.DEPENDENCIES,
        }),
    )

    provider = CacheProvider(
        url="redis://localhost",
    )

    context.register_dependency(provider)

    resolved = (
        context.runtime.container
        .resolve("cache")
    )

    assert resolved is provider
