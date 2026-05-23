from template_app.runtime.bootstrap import bootstrap_kernel


def test_single_app_source_of_truth() -> None:
    kernel = bootstrap_kernel()

    assert kernel.app is kernel._context.app
