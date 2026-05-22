from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_module_pipeline_installs_modules() -> None:
    kernel = bootstrap_application()

    names = {
        manifest.name
        for manifest in kernel.modules
    }

    assert "health" in names
