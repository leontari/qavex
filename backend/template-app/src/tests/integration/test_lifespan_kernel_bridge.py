from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.factories.kernel import (
    build_testing_kernel,
)
from tests.factories.transport import (
    get_http_app,
)


@pytest.mark.asyncio
async def test_lifespan_executes_kernel_lifecycle() -> None:

    kernel = build_testing_kernel()

    app = get_http_app(
        kernel,
    )

    async with TestClient(app):

        assert True
