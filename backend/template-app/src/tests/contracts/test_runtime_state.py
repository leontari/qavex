from __future__ import annotations

from template_app.runtime.container.container import Container
from template_app.runtime.bootstrap import bootstrap_kernel


def test_runtime_contains_container() -> None:
    kernel = bootstrap_kernel()

    assert isinstance(kernel._context.runtime.container, Container)
