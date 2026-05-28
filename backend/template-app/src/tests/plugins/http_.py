from __future__ import annotations

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from template_app.runtime.transports.http.factory import (
    create_fastapi_transport,
)

from template_app.runtime.kernel.kernel import (
    RuntimeKernel,
)


@pytest.fixture
def app(
    kernel: RuntimeKernel,
) -> FastAPI:
    return create_fastapi_transport(
        kernel=kernel,
    )


@pytest.fixture
def client(
    app: FastAPI,
) -> TestClient:
    return TestClient(app)
