from template_app.runtime.bootstrap import (
    bootstrap_kernel,
)


def test_module_pipeline_installs_modules() -> None:
    kernel = bootstrap_kernel()

    names = {
        manifest.name
        for manifest in kernel.modules
    }

    assert "health" in names
