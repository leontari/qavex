from __future__ import annotations

import os
import sys


def test_app_starts(app):
    assert app.title == "Template App"


def test_import_app():
    # Add src to PYTHONPATH
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.path.join(root, "backend/template-app/src"))

    from template_app.main import app

    assert app is not None


def test_uvicorn_import():
    import importlib

    module = importlib.import_module("template_app.main")
    assert hasattr(module, "app")


from template_app.core_.app_.factory import create_app
# тест фабрики приложения
# убедиться, что create_app() не падает без специфичных локальных путей
