from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)



def test_container_attached_to_app_state() -> None:
    context = bootstrap_application()

    assert context.app.state.container is context.container
