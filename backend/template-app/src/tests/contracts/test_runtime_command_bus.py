from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_runtime_contains_command_bus() -> None:
    kernel = bootstrap_application()

    assert kernel.context.runtime.command_bus is not None


def test_runtime_contains_query_bus() -> None:
    kernel = bootstrap_application()

    assert kernel.context.runtime.query_bus is not None
