from tests.factories.module_context import (
    build_module_context,
)


def test_module_context_does_not_expose_kernel_directly() -> None:

    ctx = build_module_context()

    # sandbox APIs are exposed
    assert hasattr(ctx, "runtime")
    assert hasattr(ctx, "infra")
    assert hasattr(ctx, "messaging")

    # kernel internals MUST stay hidden
    assert not hasattr(ctx, "_kernel")
    assert not hasattr(ctx, "_app")
    assert not hasattr(ctx, "app")
