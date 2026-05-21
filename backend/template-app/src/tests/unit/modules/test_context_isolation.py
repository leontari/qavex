from template_app.bootstrap.modules.context import (
    ModuleSetupContext,
)


def test_context_has_no_kernel_reference() -> None:

    assert "_kernel" not in ModuleSetupContext.__slots__
