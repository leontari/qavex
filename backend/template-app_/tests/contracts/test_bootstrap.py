from template_app.runtime.kernel.bootstrap import bootstrap_kernel


def test_bootstrap_application():
    context = bootstrap_kernel()

    assert context.app is not None
    assert context.container is not None
