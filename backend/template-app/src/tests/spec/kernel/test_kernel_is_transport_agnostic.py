from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.transports.http.transport import FastAPITransport


# def test_kernel_boots_without_transports(kernel: RuntimeKernel) -> None:
#     """
#     Kernel should boot without any installed transports.
#
#     Runtime kernel must remain transport-agnostic.
#     """
#     assert kernel is not None
#
#
# def test_kernel_has_no_transports_by_default(kernel: RuntimeKernel) -> None:
#     """
#     Runtime kernel should not install transports implicitly.
#     """
#     assert kernel.transports == ()
#
#
# def test_transport_manager_starts_empty(kernel: RuntimeKernel) -> None:
#     """
#     Transport manager should start without transports.
#     """
#     manager = kernel.transport_manager
#
#     assert manager.transports == ()
#
#
# def test_transport_runtime_starts_empty(kernel: RuntimeKernel) -> None:
#     """
#     Transport runtime domain should start empty.
#     """
#     transport_runtime = kernel.transport_runtime
#
#     assert transport_runtime.manager.transports == ()
#
#
# def test_kernel_does_not_depend_on_http_transport(
#     kernel: RuntimeKernel,
# ) -> None:
#     """
#     Kernel should not depend on HTTP runtime existence.
#     """
#     runtime = kernel.runtime
#
#     assert runtime.transports is not None
#
#
# def test_kernel_context_exists_without_transports(
#     kernel: RuntimeKernel,
# ) -> None:
#     """
#     Kernel context should exist independently from transport layer.
#     """
#     assert kernel.context is not None
#
#
# def test_runtime_domains_exist_without_transports(
#     kernel: RuntimeKernel,
# ) -> None:
#     """
#     Runtime domains should boot independently from transports.
#     """
#     assert kernel.lifecycle is not None
#     assert kernel.infrastructure is not None
#     assert kernel.messaging is not None
#     assert kernel.module_runtime is not None
#
#
# def test_kernel_transport_boundary_is_optional(kernel: RuntimeKernel) -> None:
#     """
#     Transport layer should remain optional boundary.
#     """
#     assert len(kernel.transports) == 0


def test_http_mode_installs_http_transport(kernel: RuntimeKernel) -> None:
    transport = kernel.transport_manager.get(FastAPITransport)

    assert transport is not None
