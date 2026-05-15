from template_app.bootstrap.runtime_ import bootstrap_application


def test_bootstrap_application():
    context = bootstrap_application()

    assert context.app is not None
    assert context.container is not None
