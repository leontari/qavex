from __future__ import annotations


def test_package_exports_app() -> None:
    import template_app

    assert hasattr(template_app, "app")
