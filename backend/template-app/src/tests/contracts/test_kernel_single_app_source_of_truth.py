from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_single_app_source_of_truth() -> None:
    kernel = bootstrap_application()

    assert kernel.app is kernel._context.app
