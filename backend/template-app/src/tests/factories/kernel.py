from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.bootstrap.kernel import ApplicationContext
from template_app.bootstrap.kernel.kernel import RuntimeKernel
from tests.factories.context import build_context, build_context_no_app
from tests.factories.runtime import build_runtime_state

if TYPE_CHECKING:
    from fastapi import FastAPI
    from template_app.bootstrap.runtime import bootstrap_application



def build_kernel_no_app() -> RuntimeKernel:
    """
    Build minimal runtime kernel.

    It doesn't contain FastaAPI transport

    This factory should be used in:
    - unit tests
    - isolated runtime tests
    - pure kernel tests

    Returns:
        RuntimeKernel: isolated kernel

    """
    context = build_context_no_app()

    kernel = RuntimeKernel(context=context)

    return kernel


def build_testing_kernel() -> RuntimeKernel:
    """
    Build fully initialized testing kernel.

    Unlike build_kernel(), this factory creates:
    - FastAPI app
    - lifecycle
    - modules
    - infrastructure
    - buses

    This factory should be used in:
    - integration tests
    - route tests
    - startup tests
    - lifecycle tests

    Returns:
        RuntimeKernel: initialized runtime
    """

    context = build_context()
    kernel = RuntimeKernel(context=context)

    return kernel


def build_testing_app() -> FastAPI:
    """
    Build initialized FastAPI testing app.

    This factory should be used in:
    - TestClient
    - API tests
    - HTTP integration

    Returns:
        FastAPI: initialized FastAPI transport

    """
    return build_testing_kernel().app
