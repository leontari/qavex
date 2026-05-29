from __future__ import annotations


def test_package_entrypoint_exposes_app() -> None:
    """Exported package app must be FastAPI-compatible ASGI app."""
    from fastapi import FastAPI
    from template_app import app

    assert isinstance(app, FastAPI)
