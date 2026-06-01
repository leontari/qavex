"""
ASGI adapter.

Important:
No composition logic allowed here.
Composition happens only in:
    KernelLauncher.build()

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.launcher import build_http_app

if TYPE_CHECKING:
    from fastapi import FastAPI

app: FastAPI = build_http_app()
