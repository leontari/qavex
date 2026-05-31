from template_app.runtime.application.builder import ApplicationBuilder


def test_builder_creates_kernel() -> None:
    builder = ApplicationBuilder()
    composition = builder.create()

    assert composition.kernel is not None
