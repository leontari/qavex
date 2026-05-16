from __future__ import annotations

from template_app.bootstrap.container import Container
from template_app.bootstrap.runtime.bootstrap import bootstrap_application


def test_runtime_contains_container() -> None:
    kernel = bootstrap_application()

    assert isinstance(kernel.context.runtime.container, Container)
