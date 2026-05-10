from __future__ import annotations

import logging

import pytest
from fastapi.testclient import TestClient
from template_app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def caplog_info(caplog):
    with caplog.at_level(logging.INFO):
        yield caplog
