from __future__ import annotations


def test_package_import() -> None:
    import template_app

    assert template_app is not None
    assert hasattr(template_app, "app")
