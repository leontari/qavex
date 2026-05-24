from __future__ import annotations

from template_app.runtime.kernel import (
    RuntimeKernel,
)
from template_app.transports.http.transport import (
    FastAPITransport,
)
from tests.factories.runtime import (
    build_runtime_state,
)
from tests.factories.transport import (
    build_test_transport,
)


def test_kernel_contains_runtime() -> None:

    runtime = build_runtime_state()

    kernel = RuntimeKernel.create(
        runtime=runtime,
    )

    assert kernel._context.runtime is runtime


def test_kernel_has_no_modules_initially() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    assert kernel.modules == ()


def test_kernel_has_no_transports_initially() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    assert kernel.transport_manager.transports == ()


def test_kernel_can_install_transport() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    transport = build_test_transport()

    kernel.install_transport(
        transport,
    )

    assert transport in kernel.transport_manager.transports


def test_kernel_can_resolve_transport() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    transport = build_test_transport()

    kernel.install_transport(
        transport,
    )

    resolved = kernel.transport_manager.get(
        type(transport),
    )

    assert resolved is transport


def test_kernel_returns_none_for_missing_transport() -> None:

    kernel = RuntimeKernel.create(
        runtime=build_runtime_state(),
    )

    transport = kernel.transport_manager.get(
        FastAPITransport,
    )

    assert transport is None
