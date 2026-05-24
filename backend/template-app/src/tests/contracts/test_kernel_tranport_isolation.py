from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.factories.runtime import build_runtime_state


def test_kernel_can_exist_without_transport() -> None:
    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    assert kernel.transports == ()
    assert kernel.transport_manager.transports == () # TODO: check if they are the same?
