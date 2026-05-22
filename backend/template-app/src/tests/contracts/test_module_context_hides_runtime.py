from tests.factories.module_context import (
    build_module_context,
)


def test_module_context_hides_runtime() -> None:

    context = build_module_context()

    assert not hasattr(context, "_context")
    assert not hasattr(context, "_kernel")
    assert not hasattr(context, "container")
    assert not hasattr(context, "_runtime")
