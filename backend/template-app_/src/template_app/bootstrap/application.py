"""Composition root."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI

from template_app.runtime.container import Container


@dataclass(slots=True)
class ApplicationContext:
    app: FastAPI
    container: Container
