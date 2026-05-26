"""ASGI entrypoint."""

# legacy, should be deleted after Make commands updates
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI

from template_app.runtime.kernel.bootstrap import bootstrap_kernel
from template_app.runtime.transports.http.factory import create_http_app

if TYPE_CHECKING:
    from fastapi import FastAPI

    from template_app.runtime.kernel.kernel import RuntimeKernel

kernel: RuntimeKernel = bootstrap_kernel()

app: FastAPI = create_http_app(kernel)
