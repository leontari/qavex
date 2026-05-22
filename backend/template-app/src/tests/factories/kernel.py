from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.kernel import RuntimeKernel
from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)
from tests.factories.runtime import build_runtime_state
from tests.factories.transport import build_test_transport


def build_isolated_kernel() -> tuple[RuntimeKernel]:
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

    return RuntimeKernel.create(
        runtime=build_runtime_state(),
        app=build_test_transport(),
        ),


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
