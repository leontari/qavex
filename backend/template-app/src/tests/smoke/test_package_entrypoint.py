from __future__ import annotations

from fastapi import FastAPI



def test_package_entrypoint_exposes_app() -> None:
    from template_app import app

    assert isinstance(app, FastAPI)
