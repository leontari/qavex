from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.application import ApplicationContext
from template_app.bootstrap.container import Container
from template_app.bootstrap.modules import MODULES


def bootstrap_application() -> ApplicationContext:
    """
    Create fully configured application runtime.

    Returns:
        ApplicationContext: the fully configured application instance

    """
    app = FastAPI(
        title="template-app",
    )

    container = Container()

    # TODO: recheck this
    app.state.container = container

    for module in MODULES:
        module.setup(app, container)

    return ApplicationContext(
        app=app,
        container=container,
    )
