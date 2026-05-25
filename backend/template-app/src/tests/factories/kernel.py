from __future__ import annotations

from fastapi import FastAPI

from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)
from template_app.runtime.kernel import (
    RuntimeKernel,
)
from template_app.runtime.transports.http import (
    create_http_app,
)
from tests.factories.runtime import (
    build_runtime_state,
)
from tests.factories.transport import (
    get_http_app,
)


def build_kernel_no_transport() -> RuntimeKernel:
    """
    Build kernel without transports.
    """

    return RuntimeKernel.create(
        runtime=build_runtime_state(),
    )


def build_isolated_kernel() -> RuntimeKernel:
    """
    Build isolated runtime kernel.
    """

    return RuntimeKernel.create(
        runtime=build_runtime_state(),
    )


def build_testing_kernel() -> RuntimeKernel:
    """
    Build initialized runtime kernel.

    Includes:
    - infrastructure
    - messaging
    - lifecycle
    - modules

    No transports installed by default.
    """

    return bootstrap_kernel()


def build_testing_http_kernel() -> RuntimeKernel:
    """
    Build initialized kernel with HTTP transport.
    """

    kernel = build_testing_kernel()

    create_http_app(
        kernel,
    )

    return kernel


def build_testing_app() -> FastAPI:
    """
    Build initialized FastAPI application.
    """

    kernel = build_testing_http_kernel()

    return get_http_app(
        kernel,
    )
