import pytest
from fastapi.testclient import TestClient
from template_app.main import app

@pytest.fixture
def client():
    return TestClient(app)
