from __future__ import annotations

from template_app.bootstrap.container import Container
from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)



def test_container_attached_to_runtime() -> None:
    context = bootstrap_application()

    assert context.runtime.container is not None
    assert isinstance(context.runtime.container, Container)
