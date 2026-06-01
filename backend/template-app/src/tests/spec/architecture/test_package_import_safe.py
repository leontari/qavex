import template_app


def test_package_does_not_export_app():
    assert not hasattr(template_app, "app")
