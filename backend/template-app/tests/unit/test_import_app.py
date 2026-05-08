import sys
import os


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
