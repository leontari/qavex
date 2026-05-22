from tests.factories.module_context import (
    build_module_context,
)


def test_module_context_hides_runtime_internals() -> None:

    context = build_module_context()

    # sandbox APIs are allowed
    assert hasattr(context, "runtime")
    assert hasattr(context, "infra")
    assert hasattr(context, "messaging")

    # runtime internals MUST stay hidden
    assert not hasattr(context, "container")
    assert not hasattr(context, "lifecycle_registry")
    assert not hasattr(context, "state")
    assert not hasattr(context, "_kernel")
