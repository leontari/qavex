from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from fastapi import FastAPI

from template_app.bootstrap.kernel import (
    ApplicationContext,
)
from tests.factories.runtime import build_runtime_state


def test_application_context_is_immutable() -> None:
    app = FastAPI()

    context = ApplicationContext(
        runtime=build_runtime_state(),
        app=app,
    )

    with pytest.raises(FrozenInstanceError):
        context.app = FastAPI()
