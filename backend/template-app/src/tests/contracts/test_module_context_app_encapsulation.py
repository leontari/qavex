from template_app.bootstrap.runtime.bootstrap import bootstrap_application
from template_app.bootstrap.modules.context import ModuleSetupContext


def test_module_context_does_not_expose_kernel_directly() -> None:
    kernel = bootstrap_application()
    ctx = ModuleSetupContext(_kernel=kernel)

    assert hasattr(ctx, "_app")
    assert not hasattr(ctx, "app")  # explicit design decision
