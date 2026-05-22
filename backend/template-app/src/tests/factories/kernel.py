from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.kernel import KernelContext
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from tests.factories.runtime import build_runtime_state

if TYPE_CHECKING:
    from fastapi import FastAPI
    from template_app.bootstrap.runtime import bootstrap_application



def build_context_no_app() -> KernelContext:
    """
    Build isolated kernel context without transport.

    Returns:
        KernelContext: runtime-only context
    """
    runtime = build_runtime_state()

    return KernelContext(
        runtime=runtime,
        app=None,
    )


def build_kernel_no_app() -> RuntimeKernel:
    """
    Build isolated runtime kernel.

    Used for:
    - unit tests
    - pure runtime tests
    - lifecycle tests
    - kernel orchestration tests

    Returns:
        RuntimeKernel: isolated kernel
    """

    return RuntimeKernel(
        context=build_context_no_app(),
    )



def build_testing_kernel() -> RuntimeKernel:
    """
    Build fully initialized application kernel.

    Uses REAL application bootstrap.

    Includes:
    - FastAPI transport
    - lifecycle
    - infrastructure
    - messaging
    - module activation

    Used for:
    - integration tests
    - API tests
    - startup/shutdown tests

    Returns:
        RuntimeKernel: initialized runtime kernel
    """

    return bootstrap_application()


def build_testing_app() -> FastAPI:
    """
    Build initialized FastAPI app.

    Used for:
    - TestClient
    - HTTP tests
    - route tests

    Returns:
        FastAPI: initialized application transport
    """

    return build_testing_kernel().app
