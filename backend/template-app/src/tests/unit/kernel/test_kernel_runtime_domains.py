from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)


def test_kernel_exposes_lifecycle_runtime() -> None:
    kernel = bootstrap_kernel()

    assert kernel.lifecycle is kernel.runtime.lifecycle


def test_kernel_exposes_infrastructure_runtime() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.infrastructure
        is kernel.runtime.infrastructure
    )


def test_kernel_exposes_messaging_runtime() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.messaging
        is kernel.runtime.messaging
    )


def test_kernel_exposes_transport_runtime() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.transport_runtime
        is kernel.runtime.transports
    )


def test_kernel_exposes_module_runtime() -> None:
    kernel = bootstrap_kernel()

    assert (
        kernel.module_runtime
        is kernel.runtime.modules
    )
