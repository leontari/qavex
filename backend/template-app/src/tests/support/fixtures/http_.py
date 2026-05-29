from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from template_app.runtime.transports.http.factory import (
    create_http_app,
)
from template_app.runtime.transports.http.transport import (
    FastAPITransport,
)


@pytest.fixture
def http_app(kernel, http_transport: FastAPITransport) -> FastAPI:
    """
    Create HTTP transport application.
    """
    return create_http_app(kernel=kernel)


@pytest.fixture
def http_client(
    http_app: FastAPI,
) -> Generator[TestClient, Any, None]:
    """
    HTTP transport testing client.
    """
    with TestClient(http_app) as client:
        yield client
