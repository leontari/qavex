from tests.support.factories.kernel import build_kernel_no_transport
from tests.support.fakes.transports import (
    FakeHttpTransport,
    FakeKafkaTransport,
)

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_kernel_supports_multiple_transports() -> None:
    kernel = build_kernel_no_transport()

    kernel.install_transport(
        FakeHttpTransport(),
    )

    kernel.install_transport(
        FakeKafkaTransport(),
    )

    assert len(kernel.transports) == 2


def test_kernel_is_transport_agnostic() -> None:
    kernel = build_kernel_no_transport()

    assert not hasattr(kernel, "app")
    assert not hasattr(kernel, "http_app")


def test_kernel_can_exist_without_transport() -> None:
    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    assert kernel.transports == ()
    assert kernel.transport_manager.transports == () # TODO: check if they are the same?
