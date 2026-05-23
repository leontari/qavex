from template_app.runtime.module.context import (
    ModuleContext,
)


def test_context_has_no_kernel_reference() -> None:

    assert "_kernel" not in ModuleContext.__slots__
