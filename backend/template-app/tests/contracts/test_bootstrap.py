from __future__ import annotations

from fastapi import FastAPI

# from template_app.bootstrap.application import ApplicationContext
# from template_app.bootstrap.container import Container
from template_app.bootstrap.runtime.bootstrap import bootstrap_application



def test_bootstrap_application_returns_context() -> None:
    context = bootstrap_application()

    assert isinstance(context, ApplicationContext)
    assert isinstance(context.app, FastAPI)
    assert isinstance(context.container, Container)
